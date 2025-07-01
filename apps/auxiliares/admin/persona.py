from django.contrib                     import admin
from apps.auxiliares.models.persona     import Persona
from django.utils.html                  import format_html




@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    
    


    class Media:
        js = ('js/autocompletar_cargo.js',)
        
    list_display        = ('nombres_apellidos','origen','cedula','cargo')

