# apps/gestion/api/prestamo.py
from ninja import Schema
from typing import List, Optional
from datetime import date

from apps.gestion.models.prestamo import Prestamo, DetallePrestamo
from apps.gestion.models.bien import Bien
from apps.auxiliares.models.dependencia import Dependencia
from apps.auxiliares.models.motivo import Motivo
from apps.gestion.schemas.bien import BienOut


# ---------- Schemas ----------
class DetallePrestamoIn(Schema):
    bien_id: int


class PrestamoIn(Schema):
    fecha_inicio: date
    fecha_final: date
    encargado: str
    ubicacion_departamento_id: int
    motivo_id: int
    bienes: List[DetallePrestamoIn]

class DetallePrestamoOut(Schema):
    id: int
    bien: BienOut   # 👈 ahora no es str, sino un objeto
    condicion_devolucion: Optional[str]


class PrestamoOut(Schema):
    id: int
    fecha_inicio: date
    fecha_final: date
    encargado: str
    ubicacion_departamento: str
    motivo: str
    fecha_devolucion: Optional[date]
    status: str
    detalles: List[DetallePrestamoOut]


