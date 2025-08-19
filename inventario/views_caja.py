# inventario/views_caja.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from .models import Caja, Venta, Producto
from .forms import CajaAperturaForm, VentaForm
from .permissions import role_and_sucursales, user_role


def _usuario_puede_en_sucursal(user, sucursal):
    """Valida si el usuario puede operar en la sucursal dada."""
    rol, sucursales = role_and_sucursales(user)
    return any(s.id == sucursal.id for s in sucursales)


@login_required
def caja_estado(request):
    """
    Vista simple para mostrar cajas del día por sucursal accesible al usuario.
    (Opcional: si no la usas en urls, puedes omitirla.)
    """
    rol, sucursales = role_and_sucursales(request.user)
    cajas = Caja.objects.filter(sucursal__in=sucursales, fecha=timezone.now().date()).order_by('-creado_en')
    return render(request, 'inventario/caja_estado.html', {
        'cajas': cajas,
        'rol': rol
    })


@login_required
def caja_abrir(request):
    """
    Abre una caja para la sucursal permitida según el rol.
    Admin/Subadmin: pueden abrir para cualquiera; Cajero/Supervisión: solo su sucursal.
    """
    rol, sucursales = role_and_sucursales(request.user)

    if request.method == 'POST':
        form = CajaAperturaForm(request.POST, user=request.user)
        if form.is_valid():
            caja = form.save(commit=False)
            if not _usuario_puede_en_sucursal(request.user, caja.sucursal):
                raise PermissionDenied("No tienes permiso para esta sucursal.")

            caja.apertura_usuario = request.user
            caja.estado = 'ABIERTA'
            caja.save()

            messages.success(request, "Caja abierta correctamente.")
            return redirect('caja_detalle', caja_id=caja.id)
    else:
        # Fecha por defecto = hoy
        form = CajaAperturaForm(user=request.user, initial={'fecha': timezone.now().date()})

    return render(request, 'inventario/caja_abrir.html', {'form': form})


@login_required
def caja_detalle(request, caja_id):
    """
    Ver detalle de una caja (ventas, estado).
    """
    caja = get_object_or_404(Caja, id=caja_id)

    if not _usuario_puede_en_sucursal(request.user, caja.sucursal):
        raise PermissionDenied("No tienes permiso para ver esta caja.")

    ventas = caja.ventas.select_related('producto').order_by('-creado_en')
    return render(request, 'inventario/caja_detalle.html', {
        'caja': caja,
        'ventas': ventas
    })


@login_required
def venta_nueva(request, caja_id):
    """
    Registrar una nueva venta sobre una caja ABIERTA.
    Solo 'Cajero' puede registrar ventas y debe ser de la misma sucursal de la caja.
    """
    caja = get_object_or_404(Caja, id=caja_id)

    # Validaciones de permisos
    if user_role(request.user) != 'Cajero':
        raise PermissionDenied("Solo el Cajero puede registrar ventas.")
    if caja.estado != 'ABIERTA':
        messages.error(request, "La caja no está ABIERTA.")
        return redirect('caja_detalle', caja_id=caja.id)
    if not _usuario_puede_en_sucursal(request.user, caja.sucursal):
        raise PermissionDenied("No tienes permiso para esta sucursal.")

    if request.method == 'POST':
        form = VentaForm(request.POST, user=request.user, caja=caja)
        if form.is_valid():
            venta = form.save(commit=False)
            venta.caja = caja
            venta.precio_unitario = venta.producto.precio
            venta.total = venta.precio_unitario * venta.cantidad
            venta.usuario = request.user
            venta.save()

            # Actualizar stock (sin bloquear ventas si hay poco stock; solo advertimos)
            producto = venta.producto
            if venta.cantidad > producto.stock:
                messages.warning(request, "Stock insuficiente. Se registró la venta, revisa inventario.")
            producto.stock = max(0, producto.stock - venta.cantidad)
            producto.save()

            messages.success(request, "Venta registrada.")
            return redirect('caja_detalle', caja_id=caja.id)
    else:
        form = VentaForm(user=request.user, caja=caja)

    return render(request, 'inventario/venta_form.html', {
        'caja': caja,
        'form': form
    })


@login_required
def caja_cerrar(request, caja_id):
    """
    Cerrar una caja ABIERTA. Por simplicidad, lo dejamos a cargo del 'Cajero'.
    (Si quieres permitir también Admin/Subadmin, amplía la condición.)
    """
    caja = get_object_or_404(Caja, id=caja_id)

    if user_role(request.user) != 'Cajero':
        raise PermissionDenied("Solo el Cajero puede cerrar la caja.")
    if caja.estado != 'ABIERTA':
        messages.error(request, "La caja no está ABIERTA.")
        return redirect('caja_detalle', caja_id=caja.id)
    if not _usuario_puede_en_sucursal(request.user, caja.sucursal):
        raise PermissionDenied("No tienes permiso para esta sucursal.")

    if request.method == 'POST':
        total_vendido = caja.ventas.aggregate(s=Sum('total'))['s'] or 0
        caja.cierre_monto = caja.apertura_monto + total_vendido
        caja.cierre_usuario = request.user
        caja.estado = 'CERRADA'
        caja.save()

        messages.success(request, "Caja cerrada correctamente.")
        return redirect('caja_detalle', caja_id=caja.id)

    total_vendido = caja.ventas.aggregate(s=Sum('total'))['s'] or 0
    esperado = caja.apertura_monto + total_vendido

    return render(request, 'inventario/caja_cerrar.html', {
        'caja': caja,
        'total_vendido': total_vendido,
        'esperado': esperado
    })
