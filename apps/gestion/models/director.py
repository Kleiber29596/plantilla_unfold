from django.db import models
from apps.auxiliares.models.persona import Persona 

class Director(models.Model):
    persona          = models.OneToOneField(Persona, on_delete=models.PROTECT, related_name='persona_info')
    resolucion       = models.CharField("Resolución DM/N°", max_length=100)
    fecha_resolucion = models.DateField("Fecha de la Resolución")
    gaceta           = models.CharField("Gaceta Oficial N°", max_length=100)
    fecha_gaceta     = models.DateField("Fecha de la Gaceta Oficial")
    fecha_designacion = models.DateField("Fecha de Designación", auto_now_add=True)

    class Meta:
        managed             =  True
        db_table            = 'gestion\".\"director'
        verbose_name        = 'Director'
        verbose_name_plural = 'Directores'

    def __str__(self):
        return f'{self.persona.nombres_apellidos}'
