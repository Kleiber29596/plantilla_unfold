from django.contrib import admin
from ..models import Subdependencia

@admin.register(Subdependencia)
class SubdependenciaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'dependencia')
    search_fields = ('nombre',)
    list_filter = ('dependencia',)
