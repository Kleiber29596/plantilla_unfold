# apps/auxiliares/api/categoria.py
from ninja import Router
from apps.auxiliares.models.categoria  import Categoria
from apps.auxiliares.schemas.categoria import CategoriaOut

router = Router(tags=["Categorias"])

@router.get("/", response=list[CategoriaOut])
def listar_categorias(request):
    return [
        CategoriaOut(id=c.id, descripcion=c.descripcion)
        for c in Categoria.objects.all()
    ]
