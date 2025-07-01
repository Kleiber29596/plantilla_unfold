from django.contrib      import admin
from django.utils.html   import format_html
from apps.gestion.models import Asignacion  # Asegúrate de importar tu modelo Asignacion
from apps.gestion.forms  import AsignacionForm


@admin.register(Asignacion)
class AsignacionAdmin(admin.ModelAdmin):
    list_display = ('bien', 'responsable', 'ubicacion',  'estatus_badge')
    list_filter = ('estatus', 'fecha_asignacion')
    search_fields = ('bien__nombre', 'responsable__nombre', 'ubicacion__nombre', 'observacion') # Ajusta según tus campos
    # form = AsignacionForm


    
    def estatus_badge(self, obj):
        if obj.estatus == 'Activo':
            return format_html('<span class="badge bg-success">{}</span>', obj.estatus)
        elif obj.estatus == 'Inactivo':
            return format_html('<span class="badge bg-danger">{}</span>', obj.estatus)
        else:
            return format_html('<span class="badge bg-secondary">{}</span>', obj.estatus)

    estatus_badge.short_description = 'Estatus'
    estatus_badge.admin_order_field = 'estatus'
   