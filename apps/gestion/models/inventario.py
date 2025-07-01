from django.db                           import models
from apps.auxiliares.models.bien         import Bien
# from apps.auxiliares.models.unidad       import Unidad
# from apps.auxiliares.models.responsable  import Responsable


class Inventario(models.Model):

    # Tipo de uso
    i = 'Individual'
    c = 'Colectivo'
    # Estados
    o = 'Operativo'
    d = 'Densicorporado'
    p = 'Prestado'

    estado  =   (
                    (o,    'Operativo'),
                    (p,    'Prestado'),
                    (d,    'Densicorporado'),
                )
    
    uso  =      (
                    (i,   'Individual'),
                    (c,   'Colectivo'),
                )


    descripcion         = models.ForeignKey(Bien, on_delete=models.PROTECT)
    # serial            = models.CharField()
    cod_bien            = models.CharField('N° de inventario del bien',unique=True)
    # cod_catalogo      = models.CharField(max_length=255)
    valor_unitario      = models.DecimalField(max_digits=10, decimal_places=2)
    estado              = models.CharField(max_length=20,   choices=estado) 
    ubicacion           = models.ForeignKey('auxiliares.Unidad', on_delete=models.PROTECT, blank=True, null=True)
    tipo_uso            = models.CharField( choices=uso, max_length=255)
    responsable         = models.ForeignKey('auxiliares.Responsable', on_delete=models.CASCADE)
    


    class Meta:
        managed             =  True
        db_table            = 'gestion\".\"inventario'
        verbose_name        = 'inventario'
        verbose_name_plural = 'inventario'

    
    def __str__(self):
        return f"{self.descripcion} - {self.cod_bien}"