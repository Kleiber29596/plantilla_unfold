from django.contrib import admin
from django.utils.html import format_html
from apps.auxiliares.models.subdependencia import Subdependencia
from apps.bien.models.detalle_asignacion import DetalleAsignacion
from django.core.exceptions import FieldError


@admin.register(Subdependencia)
class SubdependenciaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'get_bienes_count', 'reporte_directo_link')
    
    def get_bienes_count(self, obj):
        try:
            return DetalleAsignacion.objects.filter(
                devuelto=False,
                asignacion__subdependencia=obj
            ).count()
        except FieldError:
            try:
                return DetalleAsignacion.objects.filter(
                    asignacion__subdependencia=obj
                ).count()
            except Exception:
                return 0
    get_bienes_count.short_description = 'Bienes Asignados'
    
    def reporte_directo_link(self, obj):
        count = self.get_bienes_count(obj)
        if count > 0:
            # URL directa al reporte específico
            url = f"/bienes/reportes/subdependencia/{obj.id}/detallado/"
            return format_html(
                '<a class="button" href="{}" target="_blank" style="background-color: #4CAF50; color: white; padding: 5px 10px; text-decoration: none; border-radius: 3px; margin: 2px;">📊 Descargar Reporte</a>',
                url
            )
        return format_html(
            '<span style="color: #999; font-style: italic;">Sin bienes</span>'
        )
    reporte_directo_link.short_description = 'Reporte'