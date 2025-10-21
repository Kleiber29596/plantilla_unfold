from django.contrib import admin
from ..models import DetalleDevolucion

@admin.register(DetalleDevolucion)
class DetalleDevolucionAdmin(admin.ModelAdmin):
    list_display = ('devolucion', 'detalle_asignacion', 'condicion_retorno', 'fecha_retorno')
    list_filter = ('condicion_retorno', 'fecha_retorno')
