# admin.py (versión con importación)
from django.contrib import admin
from django.http import HttpResponse
from django.contrib import messages
from django.utils.html import format_html
from apps.auxiliares.models.subdependencia import Subdependencia
from unfold.admin import ModelAdmin

class SubdependenciaAdmin(ModelAdmin):
    list_display = ('nombre', 'dependencia', 'acciones_reporte')
    
    def acciones_reporte(self, obj):
        return format_html(
            '<a href="{}" class="button" style="background-color: #4CAF50; color: white; padding: 5px 10px; text-decoration: none; border-radius: 3px;">📊 Generar Reporte</a>',
            f'/bienes/reporte-subdependencia/{obj.id}/'  # Usa tu URL existente
        )
    
    acciones_reporte.short_description = 'Acciones'
    
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_id>/reporte/',
                self.admin_site.admin_view(self.redirigir_reporte),
                name='subdependencia_reporte'
            ),
        ]
        return custom_urls + urls
    
    def redirigir_reporte(self, request, object_id):
        """Redirige a la vista de reporte existente"""
        from django.shortcuts import redirect
        return redirect(f'/bienes/reporte-subdependencia/{object_id}/')

admin.site.register(Subdependencia, SubdependenciaAdmin)