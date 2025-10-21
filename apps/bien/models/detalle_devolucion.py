from django.db import models
from .devoluciones import Devolucion
from .detalle_asignacion import DetalleAsignacion
from apps.auxiliares.models import CondicionBien

class DetalleDevolucion(models.Model):
    devolucion = models.ForeignKey(Devolucion, on_delete=models.PROTECT)
    detalle_asignacion = models.ForeignKey(DetalleAsignacion, on_delete=models.PROTECT)
    condicion_retorno = models.ForeignKey(CondicionBien, on_delete=models.PROTECT)
    observaciones = models.TextField()
    fecha_retorno = models.DateField()

    class Meta:
        db_table = 'bien"."detalle_devolucion'

    def __str__(self):
        return f'Detalle de Devolucion {self.id}'
