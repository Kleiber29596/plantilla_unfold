from ninja import Router
from typing import List, Optional
from datetime import date
from django.shortcuts import get_object_or_404

from apps.auxiliares.models.motivo import Motivo
from apps.auxiliares.models.dependencia import Dependencia, Subdependencia

from ninja import Schema




# ---------- SCHEMAS ----------
class MotivoOut(Schema):
    id: int
    descripcion: str
    tipo: str
    activo: bool


class DependenciaOut(Schema):
    id: int
    nombre: str


class SubdependenciaOut(Schema):
    id: int
    nombre: str
    dependencia_id: int
    descripcion: str


# ---------- Schema IN (crear/editar responsables) ----------
class ResponsableIn(Schema):
    persona_id: int
    tipo: str
    resolucion: Optional[str] = None
    fecha_resolucion: Optional[date] = None
    gaceta: Optional[str] = None
    fecha_gaceta: Optional[date] = None
    dependencia_id: int
    subdependencia_id: Optional[int] = None

    class Config:
        from_attributes = True

# ---------- Schema OUT (detalle de un responsable) ----------
class ResponsableOut(Schema):
    id: int
    persona: str
    tipo: str
    resolucion: Optional[str] = None
    fecha_resolucion: Optional[date] = None
    gaceta: Optional[str] = None
    fecha_gaceta: Optional[date] = None
    dependencia: DependenciaOut
    subdependencia: Optional[SubdependenciaOut]  # 👈 ahora opcional

    class Config:
        from_attributes = True