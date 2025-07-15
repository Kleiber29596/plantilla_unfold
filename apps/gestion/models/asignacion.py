from django.db                          import models
from apps.auxiliares.models.bien        import Bien
from django.db.models                   import Q   # solo si usas una condición
from django.core.exceptions             import ValidationError

class Asignacion (models.Model):
   
   
   
   estatus  =      (
                    ('Activo',   'Activo'),
                    ('Inactivo', 'Inactivo'),
                )
   bien             =  models.ForeignKey(Bien,                          on_delete = models.RESTRICT )
   responsable      =  models.ForeignKey('auxiliares.Responsable',      on_delete = models.RESTRICT)
   ubicacion        =  models.ForeignKey('auxiliares.Unidad',           on_delete = models.RESTRICT, null=True, blank=True)
   fecha_asignacion =  models.DateField()
   estatus          =  models.CharField(max_length = 20, choices=estatus, default ='Activo')
   motivo           =  models.TextField(max_length = 50, null=True, blank=True)
   
   def clean(self):
        if Asignacion.objects.filter(
            bien=self.bien,
            estatus='Activo'
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                'El bien seleccionado, ya ha sido asignado a un funcionario.'
            )
   class Meta:
    managed             =  True
    db_table            = 'gestion\".\"asignacion'
    verbose_name        = 'asignacion'
    verbose_name_plural = 'asignaciones'


    def __str__(self):
        return f'{self.bien}'
    

  