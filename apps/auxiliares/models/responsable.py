from django.db                          import models
from apps.gestion.models.prestamo       import Prestamo
from apps.auxiliares.models.persona     import Persona
from apps.auxiliares.models.dependencia import Dependencia, Subdependencia


class Responsable(models.Model):
    TIPO_RESPONSABLE = [
        ("Patrimonial", "Patrimonial"),
        ("Registrador de bienes", "Registrador de bienes"),
        ("Custodio", "Custodio"),
    ]

    persona = models.ForeignKey(
        Persona,
        on_delete=models.CASCADE,
        related_name="responsabilidades"
    )
    tipo = models.CharField(max_length=50, choices=TIPO_RESPONSABLE)
    resolucion = models.CharField(max_length=100, blank=True, null=True)
    fecha_resolucion = models.DateField(blank=True, null=True)
    gaceta = models.CharField(max_length=50, blank=True, null=True)
    fecha_gaceta = models.DateField(blank=True, null=True)
    dependencia = models.ForeignKey(
        Dependencia, 
        on_delete=models.RESTRICT, 
        related_name="responsables"
    )
    subdependencia = models.ForeignKey(
        Subdependencia, 
        on_delete=models.RESTRICT, 
        related_name="responsables", 
        null=True, blank=True
    )

    class Meta:
        managed             =  True
        db_table            = 'auxiliares\".\"responsable'
        verbose_name        = 'Responsable'
        verbose_name_plural = 'Responsables'