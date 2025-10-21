from django.contrib import admin
from ..models import Asignacion, DetalleAsignacion

class DetalleAsignacionInline(admin.TabularInline):
    model = DetalleAsignacion
    extra = 1
    readonly_fields = ('fecha_retorno',)


@admin.register(Asignacion)
class AsignacionAdmin(admin.ModelAdmin):
    list_display = ('nro_asignacion', 'fecha_asignacion', 'dependencia', 'usuario', 'estatus')
    list_filter = ('estatus', 'dependencia', 'fecha_asignacion')
    fields = ('dependencia', 'subdependencia',  'usuario', 'estatus')
    readonly_fields = ('fecha_asignacion',)
    search_fields = ('usuario__nombres_apellidos', 'dependencia__nombre')
    inlines = [DetalleAsignacionInline]
