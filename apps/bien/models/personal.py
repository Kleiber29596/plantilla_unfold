from django.db import models
from apps.auxiliares.models.catalogo_bienes import Estado

class Personal(models.Model):
    origen = models.CharField(max_length=1)
    cedula = models.CharField(max_length=15)
    nombres_apellidos = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'auxiliares"."personal'
        verbose_name = 'Personal'
        verbose_name_plural = 'Personal'


    def __str__(self):
        return self.nombres_apellidos
