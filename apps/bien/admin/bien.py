from django.contrib import admin
from apps.bien.models.bien import Bien
@admin.register(Bien)
class BienAdmin(admin.ModelAdmin):
    list_display = ('codigo_bien', 'tipo_bien', 'serial', 'marca', 'modelo', 'estado')
    search_fields = ('codigo_bien', 'serial')
    list_filter = ('tipo_bien', 'marca', 'modelo', 'estado', 'condicion')