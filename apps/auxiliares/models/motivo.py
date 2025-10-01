from django.db import models


tipo_movimientos = (

    ('Desincorporación', 'Desincorporación'),
    ('Préstamo', 'Préstamo'),
    ('Reasignacion', 'Reasignacion'),
)

class Motivo(models.Model):
    descripcion = models.CharField(max_length=255)
    tipo        = models.CharField('Tipo movimiento',max_length=100, choices=tipo_movimientos) 
    activo      = models.BooleanField(default=True)

    class Meta:
        managed             =  True
        db_table            = 'auxiliares\".\"motivo'
        verbose_name        = 'Motivo'
        verbose_name_plural = 'Motivos'

    def __str__(self):
        return self.descripcion