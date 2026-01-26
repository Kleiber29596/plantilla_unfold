from django.db import models
from .dependencia import Dependencia

class Subdependencia(models.Model):
    nombre = models.CharField(max_length=100)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.PROTECT)
    
    class Meta:
        db_table = 'auxiliares"."subdependencia'

    def __str__(self):
        return self.nombre
