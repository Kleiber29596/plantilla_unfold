# apps/auxiliares/api/categoria.py
from ninja import Router
from apps.auxiliares.models.categoria  import Categoria, Subcategoria
from apps.auxiliares.schemas.categoria import CategoriaOut, SubcategoriaOut

router = Router(tags=["Categorias"])

@router.get("/", response=list[CategoriaOut])
def listar_categorias(request):
    return [
        CategoriaOut(id=c.id, descripcion=c.descripcion)
        for c in Categoria.objects.all()
    ]


@router.get("listar/", response=list[SubcategoriaOut])
def listar_subcategorias(request):
    return [
        SubcategoriaOut(id=c.id, descripcion=c.descripcion, categoria_id=c.categoria_id)
        for c in Subcategoria.objects.all()
    ]

