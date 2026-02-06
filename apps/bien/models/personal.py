from django.db import models
from apps.auxiliares.models.catalogo_bienes import Estado

class Personal(models.Model):
    V    =   'V'
    E    =   'E'

    ORIGEN  =   (
                    (V,  'V'),
                    (E,  'E'),
                )

    origen = models.CharField(max_length=1, choices=ORIGEN)
    cedula = models.CharField(max_length=15)
    nombres_apellidos = models.CharField('Nombre/Apellido',max_length=100)
    cargo = models.CharField(max_length=100)
    departamento = models.ForeignKey('auxiliares.Dependencia', on_delete=models.PROTECT, to_field='codigo')
    subdependencia = models.ForeignKey('auxiliares.Subdependencia', on_delete=models.PROTECT)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'auxiliares"."personal'
        verbose_name = 'Personal'
        verbose_name_plural = 'Personal'


    def __str__(self):
        return self.nombres_apellidos
