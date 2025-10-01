from django.db import models


class Persona(models.Model):
    V    =   'V'
    E    =   'E'

    ORIGEN  =   (
                    (V,  'V'),
                    (E,  'E'),
                )

    nacionalidad            = models.CharField('Nacionalidad',      max_length =   1,   choices = ORIGEN                            )
    cedula                  = models.IntegerField('Cédula',                                                                           )
    nombres_apellidos       = models.CharField('Nombres/Apellidos',   max_length=255)
    cargo                   = models.CharField('cargo',   max_length=100)

    class Meta:
        managed             =  True
        db_table            = 'auxiliares\".\"persona'
        verbose_name        = 'Persona'
        verbose_name_plural = 'Personas'
        


    def __str__(self):
        return f'{self.nombres_apellidos} - {self.nacionalidad} - {self.cedula}'