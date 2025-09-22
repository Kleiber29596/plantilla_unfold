from django.contrib                 import admin
from apps.gestion.models.bien       import Bien
from django.utils.html              import format_html
from apps.gestion.models.asignacion import Asignacion


class AsignacionInline(admin.TabularInline):
    model = Asignacion
    extra = 1
    verbose_name = "Asignación"
    verbose_name_plural = "Asignaciones"

@admin.register(Bien)
class BienAdmin(admin.ModelAdmin):
    # ¡Aquí está el cambio clave! Usa 'estado_badge' en lugar de 'estado'
    list_filter = ('cod_bien', 'categoria__descripcion', 'modelo', 'condicion',   'estatus',)
    fields = ['cod_bien','categoria', 'modelo', 'caracteristicas', 'tipo_uso', 'valor_unitario', 'condicion', 'estatus','fecha_adquisicion']
    list_display = ('cod_bien', 'categoria', 'modelo', 'condicion',   'estado_badge',)
    inlines = [AsignacionInline]

    def estado_badge(self, obj):
            if obj.estatus == 'Disponible':
                return format_html('<span class="badge bg-success">{}</span>', obj.estatus)
            elif obj.estatus == 'Desincorporado':
                return format_html('<span class="badge bg-danger">{}</span>', obj.estatus)
            else:
                return format_html('<span class="badge bg-secondary">{}</span>', obj.estatus)
    

    estado_badge.short_description = 'Estatus'
    estado_badge.admin_order_field = 'estatus' # Asegúrate de que esto sea el nombre del campo real en el modelo