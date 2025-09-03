from django.db                          import models
from apps.gestion.models.bien           import Bien
from django.db.models                   import Q   
from django.core.exceptions             import ValidationError
from simple_history.models              import HistoricalRecords 
from apps.auxiliares.models.dependencia import Dependencia, Subdependencia


class Asignacion (models.Model):
   
   
   
   estatus  =      (
                    ('Activa',   'Activa'),
                    ('Inactiva', 'Inactiva'),
                )
   bien             =  models.ForeignKey(Bien,                          on_delete = models.RESTRICT )
   responsable      =  models.ForeignKey('auxiliares.Responsable',      on_delete = models.RESTRICT, null=True, blank=True)
   dependencia      =  models.ForeignKey(Dependencia,           on_delete = models.RESTRICT, null=True, blank=True, related_name='h_asignacion_dependencia')
   subdependencia   =  models.ForeignKey(Subdependencia,           on_delete = models.RESTRICT, null=True, blank=True, related_name='h_asignacion_subdependencia')
   fecha_asignacion =  models.DateField()
   estatus          =  models.CharField(max_length = 20, choices=estatus, default ='Activa')
   motivo           =  models.TextField(max_length = 50, null=True, blank=True, help_text='¿Motivo de desactivación de la asignación?')
   history          =  HistoricalRecords() # Añade esta línea

   def clean(self):
        if Asignacion.objects.filter(
            bien=self.bien,
            estatus='Activa'
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                'El bien seleccionado, ya ha sido asignado a un funcionario. Desactive la asignación existente, si quiere reasignar el bien'
            )
   class Meta:
    managed             =  True
    db_table            = 'gestion\".\"asignacion'
    verbose_name        = 'asignacion'
    verbose_name_plural = 'asignaciones'


    def __str__(self):
        print("Asignacion __str__ ejecutado")  
        return f'{self.bien.cod_bien} '
    
    

  