from django.db import models
from apps.auxiliares.models.catalogo_bienes import Estado
from apps.auxiliares.models.catalogo_bienes import CondicionBien
from apps.auxiliares.models.catalogo_bienes import Color
from apps.auxiliares.models.catalogo_bienes import Marca
from apps.auxiliares.models.catalogo_bienes import Modelo
from apps.auxiliares.models.catalogo_bienes import TipoBien

class Bien(models.Model):
    codigo_bien         = models.CharField(max_length=50)
    tipo_bien           = models.ForeignKey(TipoBien, on_delete=models.PROTECT, null=True, blank=True)
    serial              = models.CharField(max_length=100)
    color               = models.ForeignKey(Color, on_delete=models.PROTECT)
    marca               = models.ForeignKey(Marca, on_delete=models.PROTECT, null=True, blank=True)
    modelo              = models.ForeignKey(Modelo, on_delete=models.PROTECT, null=True, blank=True)
    condicion           = models.ForeignKey(CondicionBien, on_delete=models.PROTECT)
    estado              = models.ForeignKey(Estado, on_delete=models.PROTECT)
    valor_unitario      = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    fecha_adquisicion   = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'bien"."bien'
        verbose_name = 'Bien'
        verbose_name_plural = 'Bienes'


    def __str__(self):
        return self.codigo_bien
