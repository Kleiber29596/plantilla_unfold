# apps/gestion/api/prestamo.py
from ninja import Schema
from typing import List, Optional
from datetime import date

from apps.gestion.models.prestamo import Prestamo, DetallePrestamo
from apps.gestion.models.bien import Bien
from apps.auxiliares.models.dependencia import Dependencia
from apps.auxiliares.models.motivo import Motivo
from apps.gestion.schemas.bien import BienOut



# ---------- Schemas de préstamo ----------

class DetallePrestamoIn(Schema):
    bien_id: int
    condicion_devolucion: Optional[str] = None

class ResponsablePrestamoIn(Schema):
    responsable_id: int
    rol: str


class PrestamoIn(Schema):
    fecha_inicio: date
    fecha_final: date
    departamento_entrega_id: Optional[int]
    departamento_recibe_id: Optional[int]
    motivo_id: int
    bienes: List[DetallePrestamoIn]
    responsables: List[ResponsablePrestamoIn]



class DetallePrestamoOut(Schema):
    id: int
    bien: BienOut   # 👈 ahora se devuelve el objeto completo
    condicion_devolucion: Optional[str]

    class Config:
        from_attributes = True

class PersonaOut(Schema):
    id: int
    cedula: int
    nombres_apellidos: str

class ResponsablePrestamoOut(Schema):
    id: int
    rol: str
    persona: PersonaOut

class PrestamoOut(Schema):
    id: int
    fecha_inicio: date
    fecha_final: date
    departamento_entrega: Optional[str]
    departamento_recibe: Optional[str]
    motivo: str
    fecha_devolucion: Optional[date]
    status: str
    detalles: List[DetallePrestamoOut]
    responsables: List[ResponsablePrestamoOut]




class ResponsablePrestamoIn(Schema):
    prestamo_id: int
    responsable_id: int
