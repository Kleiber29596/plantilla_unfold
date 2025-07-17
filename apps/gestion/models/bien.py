from django.db import models
from apps.auxiliares.models.categoria import Categoria
from apps.auxiliares.models.marca import Marca
from apps.auxiliares.models.modelo import Modelo

class Bien(models.Model):


    uso  =      (
                    ('Individual',   'Individual'),
                    ('Colectivo',    'Colectivo'),
                )

    # Estados
   
    estado  =   (
                    ('Operativo',               'Operativo'),
                    ('Desincorporado',          'Desincorporado'),

                )
    categoria            = models.ForeignKey(Categoria, verbose_name="Categoría",  on_delete=models.PROTECT)
    modelo               = models.ForeignKey(Modelo, null=True, blank=True, on_delete=models.PROTECT)
    caracteristicas      = models.TextField(null=True, blank=True)
    cod_bien             = models.CharField('codigo_de_bien', max_length=50, unique=True, help_text='Código de bien Nacional')
    tipo_uso             = models.CharField('tipo de uso', max_length=50, choices=uso,)
    valor_unitario       = models.DecimalField('valor unitario', max_digits=10, decimal_places=2, help_text='Valor unitario del bien')
    condicion            = models.CharField('condición', max_length=50, help_text='Condición del bien')
    estatus              = models.CharField('estatus', max_length=20, help_text='Estado del bien',  default='Activo', choices=estado)




    class Meta:
        managed             =  True
        db_table            = 'auxiliares\".\"bien'
        verbose_name        = 'Bien'
        verbose_name_plural = 'Bienes'

    def __str__(self):
        return f'{self.cod_bien} {self.modelo} {self.categoria} '