from django.db import models
from apps.auxiliares.models.unidad import Unidad
from apps.auxiliares.models.persona import Persona

class Responsable(models.Model):

    
    persona                 = models.OneToOneField(Persona, on_delete=models.PROTECT, related_name='datos_persona')
    unidad                  = models.ForeignKey("Unidad", null= True, blank=True, on_delete=models.PROTECT, related_name='unidad')
    
    class Meta:
        managed             =  True
        db_table            = 'auxiliares\".\"responsable'
        verbose_name        = 'Responsable'
        verbose_name_plural = 'Responsables'
        


    def __str__(self):
        return f'{self.persona.origen}-{self.persona.cedula}-{self.persona.nombres_apellidos}'