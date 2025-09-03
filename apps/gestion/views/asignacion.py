# apps/bienes/api/views.py
from typing                                   import List
from ninja                                    import Router
from apps.gestion.schemas.bien                import BienIn, BienOut, BienPatch, BienListOut
from apps.gestion.models.asignacion           import Asignacion
from django.shortcuts                         import get_object_or_404
from django.db                                import transaction
from ninja.errors                             import HttpError
from django.db.models                         import Q


router = Router(tags=["Asignaciones"])

# apps/asignaciones/api/router.py
@router.get("/listar", response=AsignacionListOut)
def listar_bienes(request, page: int = 1, page_size: int = 10, q: str = ""):
    page = max(1, page)
    page_size = min(max(1, page_size), 100)

    qs = (Asignacion.objects
          .select_related("categoria", "modelo")
          .order_by("-id"))

    if q:
        qs = qs.filter(
            Q(cod_bien__icontains=q) |
            Q(estatus__icontains=q) |
            Q(condicion__icontains=q) |
            Q(categoria__descripcion__icontains=q) |
            Q(modelo__descripcion__icontains=q)
        )

    total = qs.count()
    start = (page - 1) * page_size
    end = start + page_size

    # ⚠️ IMPORTANTE: convierte a lista antes de mapear (evita "DjangoGetter")
    page_items = list(qs[start:end])
    items = [bien_to_out(b) for b in page_items]

    return {"results": items, "total": total}