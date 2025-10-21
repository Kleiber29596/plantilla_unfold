from django.db import models

class Devolucion(models.Model):
    asignacion = models.ForeignKey('bien.Asignacion', on_delete=models.PROTECT)
    fecha_devolucion = models.DateField()
    observaciones = models.TextField()

    class Meta:
        db_table = 'bien"."devolucion'

    def __str__(self):
        return f'Devolucion {self.id} de la Asignacion {self.asignacion.id}'
