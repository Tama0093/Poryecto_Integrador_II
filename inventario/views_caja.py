# inventario/views_caja.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from .models import Caja, Venta, Producto
from .forms import CajaAperturaForm, VentaForm
from .permissions import role_and_sucursales



@login_required
def caja_estado_hoy(request):
    """
    Ver estado de las cajas del día.
    (Ver está permitido para cualquier rol autenticado con acceso a la(s) sucursal(es).)
    """
    rol, sucs = role_and_sucursales(request.user)
    hoy = timezone.now().date()

    # Admin ve todas (cámbialo a none() si no quieres que vea nada)
    if rol == 'Administrador':
        cajas = Caja.objects.filter(fecha=hoy).select_related('sucursal')
    else:
        cajas = Caja.objects.filter(fecha=hoy, sucursal__in=sucs).select_related('sucursal')

    return render(request, 'inventario/caja_estado.html', {'cajas': cajas, 'hoy': hoy})


@login_required
def caja_abrir(request):
    """
    Solo CAJERO puede abrir caja.
    """
    rol, sucs = role_and_sucursales(request.user)
    if rol != 'Cajero':
        raise PermissionDenied("Solo el Cajero puede abrir caja.")

    if request.method == 'POST':
        form = CajaAperturaForm(request.POST, user=request.user)
        if form.is_valid():
            caja = form.save(commit=False)

            # Seguridad: la sucursal debe estar permitida al cajero
            if caja.sucursal not in sucs:
                raise PermissionDenied("No puedes abrir caja en esa sucursal.")

            # Evitar 2 cajas mismo día y sucursal
            if Caja.objects.filter(sucursal=caja.sucursal, fecha=caja.fecha).exists():
                messages.error(request, "Ya existe una caja para esa sucursal en esa fecha.")
                return redirect('caja_estado_hoy')

            caja.apertura_usuario = request.user
            caja.estado = 'ABIERTA'
            caja.save()

            messages.success(request, "Caja abierta correctamente.")
            return redirect('caja_detalle', caja_id=caja.id)
    else:
        form = CajaAperturaForm(user=request.user)

    return render(request, 'inventario/caja_abrir.html', {'form': form})


@login_required
def caja_detalle(request, caja_id):
    """
    Ver detalle de una caja (ventas, estado).
    (Ver está permitido para cualquier rol con acceso a esa sucursal.)
    """
    caja = get_object_or_404(Caja, pk=caja_id)
    rol, sucs = role_and_sucursales(request.user)

    # Si no es Admin, validar que la caja sea de sus sucursales
    if rol != 'Administrador' and caja.sucursal not in sucs:
        raise PermissionDenied("No puedes ver esta caja.")

    ventas = caja.ventas.select_related('producto').order_by('-creado_en')
    return render(request, 'inventario/caja_detalle.html', {'caja': caja, 'ventas': ventas})


@login_required
def venta_nueva(request, caja_id):
    """
    Solo CAJERO puede registrar ventas en una caja ABIERTA de una sucursal permitida.
    El formulario muestra productos de todas sus sucursales, pero valida
    que el producto pertenezca a la sucursal de la caja actual.
    """
    caja = get_object_or_404(Caja, pk=caja_id, estado='ABIERTA')
    rol, sucs = role_and_sucursales(request.user)

    if rol != 'Cajero':
        raise PermissionDenied("Solo el Cajero puede registrar ventas.")
    if caja.sucursal not in sucs:
        raise PermissionDenied("No puedes vender en esta sucursal.")

    if request.method == 'POST':
        form = VentaForm(request.POST, user=request.user, caja=caja)
        if form.is_valid():
            venta = form.save(commit=False)
            venta.caja = caja
            venta.precio_unitario = venta.producto.precio
            venta.total = venta.precio_unitario * venta.cantidad
            venta.usuario = request.user
            venta.save()

            # Descontar stock (sin dejar negativo)
            p = venta.producto
            if venta.cantidad > p.stock:
                messages.warning(request, "Stock insuficiente. Se registró la venta, revisa inventario.")
            p.stock = max(0, p.stock - venta.cantidad)
            p.save()

            messages.success(request, "Venta registrada.")
            return redirect('caja_detalle', caja_id=caja.id)
    else:
        form = VentaForm(user=request.user, caja=caja)

    return render(request, 'inventario/venta_form.html', {'form': form, 'caja': caja})


@login_required
def caja_cerrar(request, caja_id):
    """
    Solo CAJERO puede cerrar caja.
    """
    caja = get_object_or_404(Caja, pk=caja_id, estado='ABIERTA')
    rol, sucs = role_and_sucursales(request.user)

    if rol != 'Cajero':
        raise PermissionDenied("Solo el Cajero puede cerrar caja.")
    if caja.sucursal not in sucs:
        raise PermissionDenied("No puedes cerrar caja en esta sucursal.")

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
