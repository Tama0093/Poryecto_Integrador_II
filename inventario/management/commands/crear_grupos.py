from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = "Crea los grupos: Administrador, Subadministrador, Cajero"

    def handle(self, *args, **options):
        grupos = ['Administrador', 'Subadministrador', 'Cajero']
        for g in grupos:
            group, created = Group.objects.get_or_create(name=g)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Grupo '{g}' creado"))
            else:
                self.stdout.write(self.style.WARNING(f"Grupo '{g}' ya existe"))
