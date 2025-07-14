from django.contrib import admin
from apps.auxiliares.models.bien import Bien
from django.utils.html import format_html


@admin.register(Bien)
class BienAdmin(admin.ModelAdmin):
    # ¡Aquí está el cambio clave! Usa 'estado_badge' en lugar de 'estado'
    list_filter = ('categoria', 'cod_bien',)
    fields = ['categoria', 'modelo', 'caracteristicas', 'tipo_uso', 'valor_unitario', 'condicion', 'estatus']
    list_display = ('categoria', 'cod_bien', 'estado_badge',)

    def estado_badge(self, obj):
            if obj.estatus == 'Operativo':
                return format_html('<span class="badge bg-success">{}</span>', obj.estatus)
            elif obj.estatus == 'Desincorporado':
                return format_html('<span class="badge bg-danger">{}</span>', obj.estatus)
            else:
                return format_html('<span class="badge bg-secondary">{}</span>', obj.estatus)

    estado_badge.short_description = 'Estatus'
    estado_badge.admin_order_field = 'estatus' # Asegúrate de que esto sea el nombre del campo real en el modelo