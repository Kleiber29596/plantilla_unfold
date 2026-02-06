from django.db import models

class Dependencia(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = 'auxiliares"."dependencia'

    def __str__(self):
        return self.nombre
