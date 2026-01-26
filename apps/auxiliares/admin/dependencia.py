from django.contrib import admin
from ..models import Dependencia
from apps.auxiliares.models.subdependencia import Subdependencia
from unfold.admin import ModelAdmin, TabularInline

class SubdependenciaInline(TabularInline):
    model = Subdependencia
    extra = 1


@admin.register(Dependencia)
class DependenciaAdmin(ModelAdmin):
    search_fields = ('nombre',)
    inlines = [SubdependenciaInline]

