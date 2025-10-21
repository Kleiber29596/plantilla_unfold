from django.contrib import admin
from ..models import Personal

@admin.register(Personal)
class PersonalAdmin(admin.ModelAdmin):
    list_display = ('nombres_apellidos', 'cedula', 'cargo', 'departamento', 'estado')
    search_fields = ('nombres_apellidos', 'cedula')
    list_filter = ('estado', 'departamento')
