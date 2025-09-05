from django.contrib import admin
from apps.auxiliares.models.dependencia import Dependencia, Subdependencia  # <-- Asegúrate de importar ambos modelos

class SubdependenciaInline(admin.TabularInline):
    # CORRECTO: Pasa la clase del modelo, no una cadena de texto.
    model = Subdependencia
    extra = 1 # Opcional: Esto añade un formulario extra en blanco para crear una nueva subdependencia.
    fields = ('nombre', 'dependencia')

class DependenciaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    inlines = [SubdependenciaInline] # Asocia el inline aquí.

class SubdependenciaAdmin(admin.ModelAdmin):
    list_display = ('nombre','dependencia')
    

admin.site.register(Dependencia, DependenciaAdmin)
# También puedes registrar la subdependencia si quieres que tenga su propia página en el admin.
admin.site.register(Subdependencia, SubdependenciaAdmin)