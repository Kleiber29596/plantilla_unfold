from django.db                    import models
from apps.gestion.models.director import Director




class Unidad(models.Model):
    descripcion      = models.CharField(max_length=255)
    tipo             = models.CharField(
    max_length       = 50,
    choices=[
            ('DG', 'Dirección General'),
            ('DL', 'Dirección de Línea'),
            ('D',  'División'),
            ('EA', 'Ente Adscrito')
        ]
    )
    unidad_padre = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='sububicaciones'
    )
    director            = models.OneToOneField(Director, on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        managed             =  True
        db_table            = 'auxiliares\".\"unidad'
        verbose_name        = 'Unidad'
        verbose_name_plural = 'Unidades'

    def __str__(self):
        return f'{self.descripcion}'
