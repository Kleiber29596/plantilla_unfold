from django.db import models

tipo_estados = (
  ('Asignacion', 'Asignacion'),
  ('Bien', 'Bien'),
  ('Devolucion', 'Devolucion'),
  ('Personal', 'Personal')
)

class Estado(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100, choices=tipo_estados)

    class Meta:
        db_table = 'catalogo_bienes"."estado'

    def __str__(self):
        return self.nombre

class CondicionBien(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'catalogo_bienes"."condicion_bien'
        verbose_name = 'Condicion de Bien'
        verbose_name_plural = 'Condiciones'


    def __str__(self):
        return self.nombre

class Color(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        db_table = 'catalogo_bienes"."color'
        verbose_name = 'Color'
        verbose_name_plural = 'Colores'


    def __str__(self):
        return self.nombre 

class Marca(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'catalogo_bienes"."marca'

    def __str__(self):
        return self.nombre or 'Sin marca'



class Modelo(models.Model):
    nombre = models.CharField(max_length=100)
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)

    class Meta:
        db_table = 'catalogo_bienes"."modelo'

    def __str__(self):
        return self.nombre if self.nombre else 'Sin modelo'




class TipoBien(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'catalogo_bienes"."tipo_bien'
        verbose_name = 'Tipo de Bien'
        verbose_name_plural = 'Tipos de Bienes'

    def __str__(self):
        return self.nombre if  self.nombre else 'Sin tipo'