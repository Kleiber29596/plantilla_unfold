from django.db                           import models
from django.utils                        import timezone
from apps.gestion.models.bien            import Bien
from apps.auxiliares.models.dependencia  import Dependencia, Subdependencia
from apps.auxiliares.models.motivo       import Motivo


class Prestamo(models.Model):
    """Registro del préstamo de un bien nacional."""

    ESTADOS_PRESTAMO = [
        ('EN_PRESTAMO', 'En préstamo'),
        ('DEVUELTO', 'Devuelto'),
        ('RETRASO', 'Retraso de préstamo'),
    ]

   
    fecha_inicio                = models.DateField(default=timezone.now)
    fecha_final                 = models.DateField()
    departamento_entrega        = models.ForeignKey(Dependencia,    on_delete=models.RESTRICT, related_name="entrega", null=True, blank=True)
    departamento_recibe         = models.ForeignKey(Dependencia,   on_delete=models.RESTRICT, related_name="recibe", null=True, blank=True)
    motivo                      = models.ForeignKey(Motivo,         on_delete=models.RESTRICT, related_name="prestamos"    )
    
    # Control de devolución
    fecha_devolucion        = models.DateField(null=True, blank=True)
    status                  = models.CharField(max_length=20, choices=ESTADOS_PRESTAMO, default="EN_PRESTAMO")
    creado                  = models.DateTimeField(auto_now_add=True)
    actualizado             = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"({self.status})"

    def marcar_devuelto(self, estado_bien="En buen estado"):
        """Método para registrar devolución."""
        self.fecha_devolucion = timezone.now().date()
        self.estado_bien_devolucion = estado_bien
        self.status = "DEVUELTO"
        self.save()

    def en_retraso(self):
        """Verifica si el préstamo está retrasado."""
        if self.status == "EN_PRESTAMO" and timezone.now().date() > self.fecha_final:
            return True
        return False

    class Meta:

        managed             = True
        db_table            = 'gestion"."prestamo'
        verbose_name        = 'préstamo'
        verbose_name_plural = 'préstamos'
        ordering            = ['-creado']







class DetallePrestamo(models.Model):
    """Detalle del préstamo: bienes involucrados."""

    CONDICION = [
        ('BUENO', 'En buen estado'),
        ('DAÑADO', 'Dañado'),
    ]

    prestamo = models.ForeignKey(Prestamo, on_delete=models.CASCADE, related_name="detalles")
    bien = models.ForeignKey(Bien, on_delete=models.PROTECT, related_name="detalles")
    condicion_devolucion = models.CharField('Condición de retorno', max_length=20, choices=CONDICION, null=True, blank=True)

    def __str__(self):
        return f"{self.bien.cod_bien} ({self.prestamo.id})"

    def marcar_devuelto(self, estado="BUENO"):
        """Marcar la devolución de este bien."""
        self.fecha_devolucion = timezone.now().date()
        self.estado_bien_devolucion = estado
        self.save()

    class Meta:
        managed             = True
        db_table            = 'gestion"."detalle_prestamo'
        verbose_name        = 'detalle de préstamo'
        verbose_name_plural = 'detalles de préstamos'
        unique_together    = ('prestamo', 'bien')
        ordering           = ['bien__cod_bien']

    

class ResponsablePrestamo(models.Model):
    """Responsables asociados a un préstamo con rol específico."""

    ROLES = [
        ("RESP_ENTREGA", "Responsable entrega"),
        ("TESTIGO_ENTREGA", "Testigo entrega"),
        ("RESP_RECIBE", "Responsable recibe"),
        ("TESTIGO_RECIBE", "Testigo recibe"),
    ]

    prestamo = models.ForeignKey(
        Prestamo, on_delete=models.CASCADE, related_name="responsables"
    )
    responsable = models.ForeignKey(
        "auxiliares.Responsable",
        on_delete=models.CASCADE,
        related_name="responsables_prestamo"
    )
    rol = models.CharField(max_length=20, choices=ROLES)

    class Meta:
        managed = True
        db_table = 'gestion"."responsable_prestamo'
        verbose_name = 'responsable de préstamo'
        verbose_name_plural = 'responsables de préstamos'

    def __str__(self):
        return f"{self.responsable.persona} - {self.get_rol_display()}"

