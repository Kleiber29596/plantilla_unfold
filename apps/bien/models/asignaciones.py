from django.db import models
from apps.auxiliares.models import  Estado
class Asignacion(models.Model):

    nro_asignacion   = models.CharField(max_length=20, unique=True, editable=False)
    fecha_asignacion = models.DateField(auto_now_add=True)
    dependencia      = models.ForeignKey('auxiliares.Dependencia', on_delete=models.PROTECT)
    subdependencia   = models.ForeignKey('auxiliares.Subdependencia', on_delete=models.PROTECT)
    usuario          = models.ForeignKey('bien.Personal', on_delete=models.PROTECT)
    observaciones    = models.TextField()
    estatus          = models.ForeignKey(Estado, on_delete=models.PROTECT, default=1)

    class Meta:
        db_table = 'bien"."asignacion'
        verbose_name = 'Asignacion'
        verbose_name_plural = 'Asignaciones'



    def save(self, *args, **kwargs):
        if not self.nro_asignacion:
            last = Asignacion.objects.order_by('-id').first()
            next_id = (last.id + 1) if last else 1
            self.nro_asignacion = f'ASIG-{next_id:06d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.nro_asignacion}'
