# apps/gestion/views/indicadores.py
from ninja import Router
from django.db.models import Count
from apps.gestion.models.bien import Bien

router = Router(tags=["indicadores"])

@router.get("/bienes/condiciones", tags=["Indicadores"])
def bienes_por_condicion(request):
    """
    Retorna el número de bienes agrupados por condición
    """
    data = (
        Bien.objects.values("condicion")
        .annotate(total=Count("id"))
        .order_by("condicion")
    )
    # Transformamos en diccionario clave -> valor
    return {item["condicion"]: item["total"] for item in data}
