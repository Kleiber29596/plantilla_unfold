from django.db import models
from .asignaciones import Asignacion
from apps.auxiliares.models import  Estado
from apps.bien.models.bien import Bien

class DetalleAsignacion(models.Model):
    asignacion = models.ForeignKey(Asignacion, on_delete=models.PROTECT)
    bien = models.ForeignKey(Bien, on_delete=models.PROTECT)
    fecha_retorno = models.DateField(null=True, blank=True)
    estatus = models.ForeignKey(Estado, on_delete=models.PROTECT)

    class Meta:
        db_table = 'bien"."detalle_asignacion'

    def __str__(self):
        return f'{self.bien.modelo} - {self.bien.marca} - {self.bien.codigo_bien}'
