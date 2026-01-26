from django.urls import path
from .views.reportes import exportar_bienes_por_dependencia_excel
from .views.reporte_especifico import exportar_bienes_por_subdependencia_excel
               

urlpatterns = [
     path('reporte-inventario/', exportar_bienes_por_dependencia_excel, name='reporte_inventario'),
     path('reporte-subdependencia/<int:subdependencia_id>/', 
         exportar_bienes_por_subdependencia_excel, 
         name='reporte_subdependencia'),

]