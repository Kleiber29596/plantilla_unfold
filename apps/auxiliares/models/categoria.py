from django.db import models

class Categoria(models.Model):
    
    descripcion         = models.CharField('Categoría', max_length=255)
    cod_catalogo        = models.CharField(max_length=255, null=True)

    
    
    class Meta:
        managed             =  True
        db_table            = 'auxiliares".\"categoria'
        verbose_name        = 'Categoria'
        verbose_name_plural = 'Categorias'
    
    def __str__(self):
        return f'{self.descripcion}'
    
    
class Subcategoria(models.Model):
    descripcion = models.CharField(max_length=255)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)

    class Meta:
        managed             =  True
        db_table            = 'auxiliares\".\"subcategoria'
        verbose_name        = 'Subcategoria'
        verbose_name_plural = 'Subcategorias'

    def __str__(self):
        return f'{self.descripcion}'

