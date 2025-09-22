from ninja import Router
from typing import List
from django.shortcuts import get_object_or_404

from apps.auxiliares.schemas.auxiliares import MotivoOut, DependenciaOut, SubdependenciaOut
from apps.auxiliares.models.motivo import Motivo
from apps.auxiliares.models.dependencia import Dependencia, Subdependencia





router = Router(tags=["Auxiliares"])




# ---------- MOTIVO ----------
@router.get("/motivos", response=List[MotivoOut])
def listar_motivos(request):
    return Motivo.objects.filter(activo=True)


# ---------- DEPENDENCIA ----------
@router.get("/dependencias", response=List[DependenciaOut])
def listar_dependencias(request):
    return Dependencia.objects.all()


# ---------- SUBDEPENDENCIA ----------
@router.get("/subdependencias/{dependencia_id}", response=List[SubdependenciaOut])
def listar_subdependencias(request, dependencia_id: int):
    dependencia = get_object_or_404(Dependencia, id=dependencia_id)
    return dependencia.subdependencias.all()
