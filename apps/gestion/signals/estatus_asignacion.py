# gestion/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.gestion.models.asignacion import Asignacion, Bien # Asegúrate de importar ambos modelos
from apps.gestion.models.bien import Bien # Asegúrate de importar ambos modelos

@receiver(post_save, sender=Asignacion)
def actualizar_estatus_bien(sender, instance, created, **kwargs):
    """
    Actualiza el estatus del Bien a 'Asignado' cuando una Asignacion
    es creada o actualizada y está activa.
    """
    if created and instance.estatus == 'Activo':
        bien = instance.bien
        if bien.estatus != 'Asignado': # Evita actualizaciones innecesarias
            bien.estatus = 'Asignado'
            bien.save()
    elif not created and instance.estatus == 'Activo':
        bien = instance.bien
        if bien.estatus != 'Asignado':
            bien.estatus = 'Asignado'
            bien.save()
    elif not created and instance.estatus == 'Inactivo':
        # Opcional: Si una asignación se desactiva, puedes considerar qué hacer con el bien.
        # Por ejemplo, podrías cambiar su estado a 'Incorporado' o dejarlo como está.
        # Por ahora, no haremos nada si se desactiva, el bien quedará 'Asignado'
        # hasta que se cree una nueva asignación para él o se cambie manualmente.
        pass