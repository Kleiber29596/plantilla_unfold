from django.db import models
from .catalogo_bienes import Estado

class Personal(models.Model):
    origen = models.CharField(max_length=1)
    cedula = models.CharField(max_length=15)
    nombres_apellidos = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT)

    class Meta:
        db_table = 'auxiliares"."personal'

    def __str__(self):
        return self.nombres_apellidos
