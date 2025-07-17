from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
import requests
from decouple       import config


@staff_member_required
def consultar_cargo(request):
    cedula = request.GET.get('cedula')
    origen = request.GET.get('origen')

    if not cedula or not origen:
        return JsonResponse({'error': 'Faltan parámetros: cedula y/o origen'}, status=400)

    url_base = config('API_OPERATIVO')
    try:
        url = f'{url_base}/nomina/trabajador/{origen}/{cedula}/'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            # Suponemos que la API retorna una lista de uno o más trabajadores
            if isinstance(data, list) and data:
                trabajador = data[0]  # Tomamos el primero de la lista
                return JsonResponse({  
                'cargo': trabajador.get('cargo', ''),
                'nombre_apellido': trabajador.get('nombre_apellido', ''),
                })
            else:
                return JsonResponse({'error': 'No se encontró información del trabajador'}, status=404)

        else:
            return JsonResponse({'error': 'No encontrado en la API'}, status=404)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
