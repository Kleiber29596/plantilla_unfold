from django.contrib import admin
from ..models import DetalleAsignacion

@admin.register(DetalleAsignacion)
class DetalleAsignacionAdmin(admin.ModelAdmin):
    list_display = ('asignacion', 'bien', 'estatus')
    list_filter = ('estatus',)
    fields = ('asignacion', 'bien', 'estatus')
    readonly_fields = ('fecha_retorno',)

