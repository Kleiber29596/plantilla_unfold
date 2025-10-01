from django.contrib import admin
from apps.auxiliares.models.categoria import Categoria, Subcategoria

class SubcategoriaInline(admin.TabularInline):
    model = Subcategoria
    extra = 1

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("descripcion",)
    inlines = [SubcategoriaInline]