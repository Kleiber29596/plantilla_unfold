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
