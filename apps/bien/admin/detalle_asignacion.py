from django.contrib import admin
from ..models import DetalleAsignacion

@admin.register(DetalleAsignacion)
class DetalleAsignacionAdmin(admin.ModelAdmin):
    list_display = ('asignacion', 'bien',)
    search_fields = ('asignacion__id', 'bien__codigo_bien')
    fields = ('asignacion', 'bien', 'estatus')
    readonly_fields = ('fecha_retorno',)

