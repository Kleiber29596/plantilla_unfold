from django.contrib import admin
from apps.auxiliares.models.modelo import Modelo

@admin.register(Modelo)
class ModeloAdmin(admin.ModelAdmin):
    list_display = ("descripcion", "marca")