from django.contrib import admin
from django.utils.html import format_html
from django.db import models
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from apps.bien.models.asignaciones import Asignacion
from apps.bien.models.detalle_asignacion import DetalleAsignacion
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.forms.widgets import WysiwygWidget


class DetalleAsignacionInline(TabularInline):
    model = DetalleAsignacion
    extra = 1
    classes = ['collapse']


@admin.register(Asignacion)
class AsignacionAdmin(ModelAdmin):
    list_display = ('usuario', 'dependencia', 'fecha_asignacion', 'nro_asignacion', 'estatus_badge_outline')
    search_fields = ('usuario__nombres_apellidos', 'dependencia__nombre', 'nro_asignacion')
    list_filter = ('fecha_asignacion', 'estatus')
    
  
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