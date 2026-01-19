from django.contrib import admin
from apps.bien.models.personal import Personal

@admin.register(Personal)
class PersonalAdmin(admin.ModelAdmin):
    list_display = ('nombres_apellidos', 'cedula', 'cargo', 'departamento', 'activo')
    search_fields = ('nombres_apellidos', 'cedula')
    list_filter = ('activo', 'departamento')
