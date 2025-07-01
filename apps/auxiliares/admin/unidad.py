from django.contrib import admin
from apps.auxiliares.models.unidad import Unidad

@admin.register(Unidad)
class UnidadAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'tipo', 'unidad_padre')  # Campos visibles en la lista
    list_filter = ('tipo',)  # Filtro por tipo de ubicación
    search_fields = ('descripcion',)  # Búsqueda por nombre
