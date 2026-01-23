from django.contrib import admin
from apps.bien.models.bien import Bien
from django.utils.html import format_html
from unfold.admin import ModelAdmin


@admin.register(Bien)
class BienAdmin(ModelAdmin):
    list_display = ('codigo_bien', 'tipo_bien', 'serial', 'marca', 'modelo', 'condicion_badge_outline', 'estatus_badge_outline')
    search_fields = ('codigo_bien', 'serial')
    list_filter = ('tipo_bien', 'marca', 'modelo', 'estado', 'condicion')

    def estatus_badge_outline(self, obj):
        # Badges con borde y texto coloreado
        status_colors = {
            'En mantenimiento': {
                'light': 'border border-amber-500 text-amber-600',
                'dark': 'dark:border-amber-400 dark:text-amber-300'
            },
            'Disponible': {
                'light': 'border border-green-600 text-green-700',
                'dark': 'dark:border-green-500 dark:text-green-300'
            },
            'Desincorporado': {
                'light': 'border border-red-600 text-red-700',
                'dark': 'dark:border-red-500 dark:text-red-300'
            },
            'Asignado': {
                'light': 'border border-blue-600 text-blue-700',
                'dark': 'dark:border-blue-500 dark:text-blue-300'
            },
            '': {
                'light': 'border border-purple-600 text-purple-700',
                'dark': 'dark:border-purple-500 dark:text-purple-300'
            },
        }
        
        config = status_colors.get(obj.estado.nombre, {
            'light': 'border border-gray-600 text-gray-700',
            'dark': 'dark:border-gray-500 dark:text-gray-300'
        })
        
        classes = f"{config['light']} {config['dark']}"
        
        return format_html(
            '<span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-transparent {}">{}</span>',
            classes,
            obj.estado.nombre
        )
    
    estatus_badge_outline.short_description = 'Estatus'

    def condicion_badge_outline(self, obj):
        # Badges con borde y texto coloreado
        condicion_colors = {
            'En mantenimiento': {
                'light': 'border border-amber-500 text-amber-600',
                'dark': 'dark:border-amber-400 dark:text-amber-300'
            },
            'Bueno': {
                'light': 'border border-green-600 text-green-700',
                'dark': 'dark:border-green-500 dark:text-green-300'
            },
            'Dañado': {
                'light': 'border border-red-600 text-red-700',
                'dark': 'dark:border-red-500 dark:text-red-300'
            },
            'Regular': {
                'light': 'border border-blue-600 text-blue-700',
                'dark': 'dark:border-blue-500 dark:text-blue-300'
            },
            '': {
                'light': 'border border-purple-600 text-purple-700',
                'dark': 'dark:border-purple-500 dark:text-purple-300'
            },
        }

        config = condicion_colors.get(obj.condicion.nombre, {
            'light': 'border border-gray-600 text-gray-700',
            'dark': 'dark:border-gray-500 dark:text-gray-300'
        })
        
        classes = f"{config['light']} {config['dark']}"
        
        return format_html(
            '<span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-transparent {}">{}</span>',
            classes,
            obj.condicion.nombre
        )

    condicion_badge_outline.short_description = 'Condición'