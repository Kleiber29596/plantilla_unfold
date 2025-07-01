from django.contrib import admin
from apps.auxiliares.models.categoria import Categoria

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("descripcion",)
