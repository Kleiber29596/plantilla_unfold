from ninja import Router
from typing import List
from django.shortcuts import get_object_or_404
from apps.auxiliares.schemas.auxiliares import MotivoOut, DependenciaOut, SubdependenciaOut, ResponsableOut
from apps.auxiliares.models.motivo import Motivo
from apps.auxiliares.models.dependencia import Dependencia, Subdependencia
from apps.auxiliares.models.responsable import Responsable
from django.db.models                   import F





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

# -------- RESPONSABLES ------------
@router.get("/responsables", response=List[ResponsableOut])
def listar_responsables(request):
    responsables = Responsable.objects.select_related("persona", "dependencia", "subdependencia")

    salida = []
    for r in responsables:
        salida.append({
            "id": r.id,
            "persona": str(r.persona),  # 👈 conversión explícita
            "tipo": r.tipo,
            "resolucion": r.resolucion,
            "fecha_resolucion": r.fecha_resolucion,
            "gaceta": r.gaceta,
            "fecha_gaceta": r.fecha_gaceta,
            "dependencia": r.dependencia,
            "subdependencia": r.subdependencia,  # Puede ser None
        })
    return salida