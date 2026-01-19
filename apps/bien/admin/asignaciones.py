from django.contrib import admin
from ..models import Asignacion, DetalleAsignacion

class DetalleAsignacionInline(admin.TabularInline):
    model = DetalleAsignacion
    title = "Bienes"
    extra = 1
    readonly_fields = ('fecha_retorno',)


@admin.register(Asignacion)
class AsignacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'dependencia', 'fecha_asignacion', 'nro_asignacion',  'estatus')
    list_filter = ('estatus__nombre', 'dependencia__nombre', 'fecha_asignacion', 'usuario__nombres_apellidos')
    fields = ('dependencia', 'subdependencia',  'usuario', 'estatus')
    readonly_fields = ('fecha_asignacion',)
    search_fields = ('usuario__nombres_apellidos', 'dependencia__nombre')
    inlines = [DetalleAsignacionInline]
