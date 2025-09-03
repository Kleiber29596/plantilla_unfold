from django.db import models

class Dependencia(models.Model):
    """
    Representa una dependencia principal dentro de una organización.
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Dependencia")

    class Meta:
        managed             =  True
        db_table            = 'auxiliares".\"dependencia'
        verbose_name = "Dependencia"
        verbose_name_plural = "Dependencias"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre}"


class Subdependencia(models.Model):
    """
    Representa una subdependencia que pertenece a una dependencia principal.
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Subdependencia")
    # Esta es la relación de clave foránea
    dependencia = models.ForeignKey(
        Dependencia,
        on_delete=models.PROTECT,
        related_name='subdependencias',
        verbose_name="Dependencia a la que pertenece"
    )
    descripcion = models.TextField(blank=True, verbose_name="Descripción")

    class Meta:
        managed             =  True
        db_table            = 'auxiliares".\"subdependencia'
        verbose_name = "Subdependencia"
        verbose_name_plural = "Subdependencias"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre}"