# apps/gestion/urls.py
from django.urls              import path
from .                        import views
from django.urls              import path, include
from apps.gestion.views.reporte_general       import reporte_general 

urlpatterns = [
    path('reporte-general/', reporte_general, name='reporte_general'),
    # Puedes agregar más rutas aquí
]
