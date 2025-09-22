from ninja import Router
from typing import List
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
