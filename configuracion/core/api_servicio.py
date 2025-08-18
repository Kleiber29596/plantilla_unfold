from ninja import Router
from django.http import JsonResponse

router = Router()

@router.get("/api_servicio",  tags=["Servicio"])
def api_servicio(request):
    return JsonResponse({"status": "Servicio disponible"}, status=200)
