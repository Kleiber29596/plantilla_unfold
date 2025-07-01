from django.contrib                     import admin
from apps.auxiliares.models.responsable import Responsable
from apps.gestion.models.asignacion     import Asignacion
from django.utils.html                  import format_html
from django.urls                        import reverse
from django.utils.safestring            import mark_safe
from apps.auxiliares.forms              import ResponsableForm


class AsignacionInline(admin.TabularInline):
    model = Asignacion
    extra = 0
    fields = ('bien', 'ubicacion', 'fecha_asignacion','estatus')  # Ajusta los campos visibles
    # readonly_fields = fields  
    # can_delete = False  

    def descripcion(self, obj):
        return f"{obj.descripcion.categoria} {obj.descripcion.modelo} {obj.descripcion.descripcion}"


@admin.register(Responsable)
class ResponsableAdmin(admin.ModelAdmin):

    def generar_reporte(self, obj):
        url = reverse("reporte_bienes", args=[obj.id])
        return mark_safe(f'<a class="btn btn-secondary btn-sm" href="{url}"><i class="fas fa-print" title="Generar reporte"></i></a>')

    def nombre(self, obj):
        return f"{obj.persona.nombres_apellidos}"
    

    generar_reporte.short_description = "Reporte"
   
    class Media:
        js = ('js/autocompletar_cargo.js',)
        
    list_display        = ('nombre','unidad','generar_reporte')
    list_filter         = ('unidad',)
    form                = ResponsableForm

    inlines = [AsignacionInline]




   

