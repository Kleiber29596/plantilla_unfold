from django.contrib import admin
from apps.auxiliares.models.marca import Marca

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ("descripcion",)