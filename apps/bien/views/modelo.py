# apps/auxiliares/api/modelo.py
from ninja import Router
from apps.auxiliares.models.modelo  import Modelo
from apps.auxiliares.schemas.modelo import ModeloOut

router = Router(tags=["Modelos"])

@router.get("/", response=list[ModeloOut])
def listar_modelos(request):
    return [
        ModeloOut(id=m.id, descripcion=m.descripcion, marca=str(m.marca))
        for m in Modelo.objects.select_related("marca").all()
    ]
