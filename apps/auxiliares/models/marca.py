from django.db import models

class Marca(models.Model):
    descripcion = models.CharField(max_length=255)

    class Meta:
        managed             =  True
        db_table            = 'auxiliares\".\"marca'
        verbose_name        = 'Marca'
        verbose_name_plural = 'Marcas'

    def __str__(self):
        return self.descripcion