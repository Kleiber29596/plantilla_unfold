from django.db import models
from apps.auxiliares.models.dependencia import Subdependencia, Dependencia
from apps.auxiliares.models.persona import Persona

class Responsable(models.Model):

    
    persona                 = models.OneToOneField(Persona, on_delete=models.PROTECT, related_name='datos_persona')
    dependencia             = models.ForeignKey(Dependencia, null= True, blank=True, on_delete=models.PROTECT, related_name='dependencia')
    subdependencia          = models.ForeignKey(Subdependencia, null= True, blank=True, on_delete=models.PROTECT, related_name='subdependencia')
    
    class Meta:
        managed             =  True
        db_table            = 'auxiliares\".\"responsable'
        verbose_name        = 'Responsable'
        verbose_name_plural = 'Responsables'
        


    def __str__(self):
        return f'{self.persona.nombres_apellidos}'