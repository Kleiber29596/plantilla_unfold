from django.contrib      import admin
from django.utils.html   import format_html
from apps.gestion.models import Asignacion  # Asegúrate de importar tu modelo Asignacion
from apps.gestion.forms  import AsignacionForm

@admin.register(Asignacion)
class AsignacionAdmin(admin.ModelAdmin):
    list_display = ('bien', 'responsable', 'ubicacion',  'estatus_badge')
    list_filter = ('estatus', 'fecha_asignacion','ubicacion', 'bien__cod_bien', 'responsable__persona__cedula')
    search_fields = ('bien', 'ubicacion', 'observacion') # Aj0000000usta según tus campos
    form = AsignacionForm
    class Media:
        js = (
            'js/deshabilitar_asignacion.js', # Ruta a tu archivo JavaScript
        )
    
    # def get_readonly_fields(self, request, obj=None):

    #     if obj and obj.estatus != 'Inactivo':
    #         # (por ejemplo, es 'Inactivo', 'Pendiente', etc.)
    #         return self.readonly_fields + ('motivo',)
    #     elif obj and obj.estatus != 'Activo':
    #         return self.readonly_fields
    #     else:
    #         return self.readonly_fields + ('motivo',)
    
    def estatus_badge(self, obj):
        if obj.estatus == 'Activo':
            return format_html('<span class="badge bg-success">{}</span>', obj.estatus)
        elif obj.estatus == 'Inactivo':
            return format_html('<span class="badge bg-danger">{}</span>', obj.estatus)
        else:
            return format_html('<span class="badge bg-secondary">{}</span>', obj.estatus)

    estatus_badge.short_description = 'Estatus'
    estatus_badge.admin_order_field = 'estatus'
   