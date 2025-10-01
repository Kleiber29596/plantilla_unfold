# apps/gestion/signals.py

from django.db.models.signals           import post_save
from django.dispatch                    import receiver
from apps.gestion.models.prestamo       import DetallePrestamo
from apps.gestion.models.bien           import Bien

@receiver(post_save, sender=DetallePrestamo)
def actualizar_estatus_bien(sender, instance, created, **kwargs):
    """
    Gestiona el estatus del bien cuando se crea o actualiza un DetallePrestamo.
    """
    # Si se crea un nuevo DetallePrestamo, cambia el estatus del bien a 'Prestado'.
    if created:
        bien = instance.bien
        bien.estatus = 'Prestado'
        bien.save()

    # Si se actualiza un DetallePrestamo y se establece la condición de devolución, 
    # cambia el estatus del bien a 'Disponible'.
    elif not created and instance.condicion_devolucion:
        bien = instance.bien
        bien.estatus = 'Disponible'
        bien.save()