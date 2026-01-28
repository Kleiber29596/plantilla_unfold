from django.contrib import admin
from apps.bien.models.personal import Personal
from unfold.admin import ModelAdmin

@admin.register(Personal)
class PersonalAdmin(ModelAdmin):
    list_display = ('nombres_apellidos', 'nro_de_documento', 'cargo', 'departamento', 'subdependencia', 'activo')
    search_fields = ('nombres_apellidos', 'cedula')
    list_filter = ('activo', 'departamento','subdependencia__nombre')

    class Media:
        js = ('js/autocompletar_cargo.js',)
        
    def nro_de_documento(self, obj):
        return f'{obj.origen}-{obj.cedula}'



