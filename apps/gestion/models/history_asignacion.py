from django.db                          import models
from apps.auxiliares.models.bien        import Bien
from django.db.models                   import Q   # solo si usas una condición
from django.core.exceptions             import ValidationError


class HistoricoAsignacion (models.Model):
   
   
   OPERACIONES =   (
                        ('+', 'INSERCIÓN'),
                        ('~', 'MODIFICACIÓN')
                    )
    
   history_id                      = models.AutoField(primary_key=True)
   history_date                    = models.DateTimeField('Fecha',)
   history_change_reason           = models.CharField(max_length=100, blank=True, null=True)
   history_type                    = models.CharField('Operación', max_length=1, choices = OPERACIONES)
   estatus  =      (
                    ('Activo',   'Activo'),
                    ('Inactivo', 'Inactivo'),
                )
   bien             =  models.ForeignKey(Bien,                          on_delete = models.RESTRICT )
   responsable      =  models.ForeignKey('auxiliares.Responsable',      on_delete = models.RESTRICT)
   ubicacion        =  models.ForeignKey('auxiliares.Unidad',           on_delete = models.RESTRICT, null=True, blank=True)
   fecha_asignacion =  models.DateField()
   estatus          =  models.CharField(max_length = 20, choices=estatus, default ='Activo')
   motivo           =  models.TextField(max_length = 50, null=True, blank=True, help_text='¿Motivo de desactivación de la asignación?')

  
   class Meta:
    managed             =  False
    db_table            = 'public\".\"gestion_historicalasignacion'
    verbose_name        = 'asignacion'
    verbose_name_plural = 'asignaciones'


   
    

  