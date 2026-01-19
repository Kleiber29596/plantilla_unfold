from django.urls import path
from .views.reportes import exportar_bienes_por_responsable_excel
from .views.reporte_especifico import vista_seleccion_subdependencia, exportar_bienes_por_subdependencia_detallado

urlpatterns = [
    path('reportes/bienes_por_responsable/', exportar_bienes_por_responsable_excel, name='reporte_bienes_responsable'),
    
    # Vista para seleccionar subdependencia
    path('reportes/seleccionar-subdependencia/',
         vista_seleccion_subdependencia,
         name='seleccion_subdependencia_reporte'),
    
    # Reporte específico por subdependencia (AÑADE ESTA LÍNEA)
    path('reportes/subdependencia/<int:subdependencia_id>/detallado/',
         exportar_bienes_por_subdependencia_detallado,
         name='reporte_subdependencia_detallado'),
]