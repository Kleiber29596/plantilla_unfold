from django.db import models
from apps.auxiliares.models.marca import Marca

class Modelo(models.Model):
    descripcion = models.CharField(max_length=255)
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)

    class Meta:
        managed             =  True
        db_table            = 'auxiliares\".\"modelo'
        verbose_name        = 'Modelo'
        verbose_name_plural = 'Modelos'

    def __str__(self):
        return f'Modelo: {self.descripcion} Marca: {self.marca}'