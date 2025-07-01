from django.contrib                     import admin
from apps.gestion.models.director       import Director
from apps.auxiliares.models.responsable import Responsable

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = (
        'get_nombre_completo',
        'get_cedula',
       
    )
 
    def get_nombre_completo(self, obj):
        return f"{obj.persona.nombres_apellidos}"
    get_nombre_completo.short_description = 'Nombre del Director'

    def get_cedula(self, obj):
        return f"{obj.persona.origen}-{obj.persona.cedula}"
    get_cedula.short_description = 'Cédula'