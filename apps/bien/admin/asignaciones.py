from django.contrib import admin
from django.utils.html import format_html
from django.db import models
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from apps.auxiliares.models.catalogo_bienes import Estado

from apps.bien.models.asignaciones import Asignacion
from apps.bien.models.detalle_asignacion import DetalleAsignacion
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.forms.widgets import WysiwygWidget
from apps.auxiliares.models.dependencia import Dependencia
from apps.auxiliares.models.subdependencia import Subdependencia


class DetalleAsignacionInline(TabularInline):
    model = DetalleAsignacion
    extra = 1
    tab = True
    verbose_name = 'Bien'
    verbose_name_plural = 'Bienes'    


@admin.register(Asignacion)

class AsignacionAdmin(ModelAdmin):
    list_display = ('usuario', 'subdependencia', 'fecha_asignacion', 'nro_asignacion', 'estatus_badge_outline')
    search_fields = ('usuario__nombres_apellidos', 'dependencia__nombre', 'nro_asignacion', 'subdependencia__nombre')
    list_filter = ('fecha_asignacion', 'estatus', 'subdependencia__nombre')
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Filtramos estatus solo en el inline si es necesario
        if db_field.name == "estatus":
            # Si quieres también filtrar en el inline
            kwargs["queryset"] = Estado.objects.filter(tipo='Asignacion')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

  
    inlines = [DetalleAsignacionInline]
    
   

    
    def estatus_badge_outline(self, obj):
        status_colors = {
            'Pendiente': {
                'light': 'border border-amber-500 text-amber-600',
                'dark': 'dark:border-amber-400 dark:text-amber-300'
            },
            'Activa': {
                'light': 'border border-green-600 text-green-700',
                'dark': 'dark:border-green-500 dark:text-green-300'
            },
            'Rechazado': {
                'light': 'border border-red-600 text-red-700',
                'dark': 'dark:border-red-500 dark:text-red-300'
            },
            'Finalizada': {
                'light': 'border border-blue-600 text-blue-700',
                'dark': 'dark:border-blue-500 dark:text-blue-300'
            },
            'En Proceso': {
                'light': 'border border-purple-600 text-purple-700',
                'dark': 'dark:border-purple-500 dark:text-purple-300'
            },
        }
        
        config = status_colors.get(obj.estatus.nombre, {
            'light': 'border border-gray-600 text-gray-700',
            'dark': 'dark:border-gray-500 dark:text-gray-300'
        })
        
        classes = f"{config['light']} {config['dark']}"
        
        return format_html(
            '<span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-transparent {}">{}</span>',
            classes,
            obj.estatus.nombre
        )
    
    estatus_badge_outline.short_description = 'Estatus'

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        
        # Obtener parámetros de la URL
        usuario_id = request.GET.get('usuario')
        dependencia_id = request.GET.get('dependencia')
        subdependencia_id = request.GET.get('subdependencia')
        
        # Precargar usuario si se proporciona
        if usuario_id:
            from apps.bien.models.personal import Personal
            try:
                usuario = Personal.objects.get(id=usuario_id)
                initial['usuario'] = usuario
            except Personal.DoesNotExist:
                pass
        
        # Precargar dependencia si se proporciona
        if dependencia_id:
            # Ajusta la importación según tu modelo de Dependencia
            try:
                dependencia = Dependencia.objects.get(id=dependencia_id)
                initial['dependencia'] = dependencia
            except Dependencia.DoesNotExist:
                pass
        
        # Precargar subdependencia si se proporciona
        if subdependencia_id:
            # Ajusta la importación según tu modelo de Subdependencia
           
            try:
                subdependencia = Subdependencia.objects.get(id=subdependencia_id)
                initial['subdependencia'] = subdependencia
            except Subdependencia.DoesNotExist:
                pass
        
        return initial
    
    # Opcional: Puedes también sobrescribir el método add_view para agregar contexto extra
    def add_view(self, request, form_url='', extra_context=None):
        if extra_context is None:
            extra_context = {}
        
        # Obtener el usuario desde la URL
        usuario_id = request.GET.get('usuario')
        if usuario_id:
            try:
                from apps.bien.models.personal import Personal
                usuario = Personal.objects.get(id=usuario_id)
                extra_context['usuario_seleccionado'] = usuario
            except Personal.DoesNotExist:
                pass
        
        return super().add_view(request, form_url, extra_context)