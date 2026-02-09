from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, mark_safe
from django.utils.translation import gettext_lazy as _

from unfold.admin import ModelAdmin

from apps.bien.models.personal import Personal
from apps.bien.models.asignaciones import Asignacion
from apps.bien.models.detalle_asignacion import DetalleAsignacion

@admin.register(Personal)
class PersonalAdmin(ModelAdmin):
    list_display = (
        'nombres_apellidos', 
        'cedula_completa', 
        'cargo', 
        'departamento', 
        'estado_badge',
        'bienes_asignados_badge',
        'acciones_rapidas'
    )
    
    list_display_links = ('nombres_apellidos',)
    
    search_fields = ('nombres_apellidos', 'cedula', 'cargo')
    search_help_text = "Buscar por nombre, cédula o cargo"
    
    list_filter = (
        'activo',
        'departamento',
        'subdependencia',
    )
    
    list_filter_submit = True
    
    # Solo lectura para campos que mostraremos como HTML
    readonly_fields = ('informacion_bienes',)
    
    # Fieldsets más simple
    fieldsets = (
        (_('Información Personal'), {
            'fields': (
                ('origen', 'cedula'),
                'nombres_apellidos',
                'cargo',
            ),
        }),
        (_('Ubicación Laboral'), {
            'fields': (
                'departamento',
                'subdependencia',
                'activo',
            ),
        }),
    )
    
    # Agregamos el campo de información de bienes a los fieldsets
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        
        # Si estamos editando un objeto existente, agregamos la sección de bienes
        if obj and obj.pk:
            fieldsets = fieldsets + (
                (_('Bienes Asignados'), {
                    'fields': ('informacion_bienes',),
                    'description': _('Información sobre los bienes asignados a este personal'),
                    'classes': ('wide',),
                }),
            )
        
        return fieldsets
    
    # Métodos para display en lista
    def cedula_completa(self, obj):
        return f'{obj.origen}-{obj.cedula}'
    cedula_completa.short_description = _('Cédula')
    cedula_completa.admin_order_field = 'cedula'
    
    @admin.display(description=_('Estado'))
    def estado_badge(self, obj):
        if obj.activo:
            return "Activo"
        return "Inactivo"
    
    @admin.display(description=_('Bienes'))
    def bienes_asignados_badge(self, obj):
        count_activos = DetalleAsignacion.objects.filter(
            asignacion__usuario=obj,
            devuelto=False
        ).count()
        
        if count_activos > 0:
            return f"{count_activos} activo(s)"
        return "Sin bienes"
    
    @admin.display(description=_('Acciones'))
    def acciones_rapidas(self, obj):
        # Construir URL con todos los parámetros
        base_url = reverse('admin:bien_asignacion_add')
        params = []
        
        # Agregar usuario
        params.append(f'usuario={obj.id}')
        
        # Agregar dependencia (departamento) si existe
        if obj.departamento:
            params.append(f'dependencia={obj.departamento.id}')
        
        # Agregar subdependencia si existe
        if obj.subdependencia:
            params.append(f'subdependencia={obj.subdependencia.id}')
        
        query_string = '?' + '&'.join(params)
        
        return format_html(
            '''
            <div style="display: flex; gap: 0.25rem;">
                <a href="{}" 
                style="display: inline-flex; align-items: center; 
                        padding: 0.25rem 0.5rem; border-radius: 0.375rem; 
                        font-size: 0.75rem; font-weight: 500; 
                        border: 1px solid #d1d5db; text-decoration: none;">
                    Ver
                </a>
                <a href="{}" 
                style="display: inline-flex; align-items: center; 
                        padding: 0.25rem 0.5rem; border-radius: 0.375rem; 
                        font-size: 0.75rem; font-weight: 500; 
                        border: 1px solid #a5b4fc; text-decoration: none;">
                    Asignar
                </a>
            </div>
            ''',
            reverse('admin:bien_personal_change', args=[obj.id]),
            base_url + query_string
        )
    
    def informacion_bienes(self, obj):
        """Muestra información de bienes asignados en el formulario"""
        if not obj or not obj.pk:
            return "Guardar primero para ver bienes asignados"
        
        # Obtener bienes asignados
        bienes_asignados = DetalleAsignacion.objects.filter(
            asignacion__usuario=obj
        ).select_related(
            'asignacion', 
            'bien',
            'asignacion__dependencia',
            'asignacion__subdependencia'
        ).order_by('-asignacion__fecha_asignacion', 'devuelto')
        
        total_activos = bienes_asignados.filter(devuelto=False).count()
        total_devueltos = bienes_asignados.filter(devuelto=True).count()
        total = bienes_asignados.count()
        
        # Construir HTML - SIN indicadores/emojis
        
        
        if bienes_asignados.exists():
            html = '''
            <div style="overflow-x: auto; margin-bottom: 3rem;">
                <table style="width: 100%; border-collapse: collapse; font-size: 0.875rem; min-width: 600px;">
                    <thead>
                        <tr style="background-color: #f9fafb; border-bottom: 2px solid #e5e7eb;">
                            <th style="padding: 0.75rem; text-align: left; font-weight: 600; color: #374151;">Asignación</th>
                            <th style="padding: 0.75rem; text-align: left; font-weight: 600; color: #374151;">Código</th>
                            <th style="padding: 0.75rem; text-align: left; font-weight: 600; color: #374151;">Tipo</th>
                            <th style="padding: 0.75rem; text-align: left; font-weight: 600; color: #374151;">Marca</th>
                            <th style="padding: 0.75rem; text-align: left; font-weight: 600; color: #374151;">Modelo</th>
                            <th style="padding: 0.75rem; text-align: left; font-weight: 600; color: #374151;">Condición</th>
                            <th style="padding: 0.75rem; text-align: left; font-weight: 600; color: #374151;">Estado</th>
                        </tr>
                    </thead>
                    <tbody>
            '''
            
            for detalle in bienes_asignados:
                # Obtener valores del bien con valores por defecto
                codigo = getattr(detalle.bien, 'codigo_bien', 'N/A')
                
                # Tipo - asumiendo que tienes algún campo para tipo, sino usar descripción
                tipo = getattr(detalle.bien, 'tipo_bien', 
                             getattr(detalle.bien, 'descripcion', 'No especificado'))
                
                marca = getattr(detalle.bien, 'marca', 'No especificada')
                modelo = getattr(detalle.bien, 'modelo', 'No especificado')
                condicion = getattr(detalle.bien, 'condicion', 
                                   getattr(detalle.bien, 'estado', 'No especificada'))
                
                estado = "Activo" if not detalle.devuelto else "Devuelto"
                
                html += f'''
                        <tr style="border-bottom: 1px solid #e5e7eb;">
                            <td style="padding: 0.75rem;">
                                <div style="font-weight: 500; color: #374151;">
                                    {detalle.asignacion.nro_asignacion}
                                </div>
                                <div style="font-size: 0.75rem; color: #6b7280;">
                                    {detalle.asignacion.fecha_asignacion.strftime("%d/%m/%Y")}
                                </div>
                            </td>
                            <td style="padding: 0.75rem; color: #374151;">
                                {codigo}
                            </td>
                            <td style="padding: 0.75rem; color: #374151;">
                                {tipo}
                            </td>
                            <td style="padding: 0.75rem; color: #374151;">
                                {marca}
                            </td>
                            <td style="padding: 0.75rem; color: #374151;">
                                {modelo}
                            </td>
                            <td style="padding: 0.75rem; color: #374151;">
                                {condicion}
                            </td>
                            <td style="padding: 0.75rem; color: #374151;">
                                {estado}
                            </td>
                        </tr>
                '''
            
            html += '''
                    </tbody>
                </table>
            </div>
            '''
        else:
            html = '''
            <div style="text-align: center; padding: 2rem; background-color: #f9fafb; border-radius: 0.5rem; border: 1px solid #e5e7eb; margin-bottom: 3rem;">
                <h4 style="font-size: 1.125rem; font-weight: 600; color: #111827; margin-bottom: 0.5rem;">
                    No hay bienes asignados
                </h4>
                <p style="color: #6b7280; margin-bottom: 1.5rem;">
                    Este personal no tiene bienes asignados actualmente.
                </p>
            </div>
            '''
        
        return mark_safe(html)
    
    informacion_bienes.short_description = _('Información de Bienes Asignados')
    
    class Media:
        js = ('js/autocompletar_cargo.js',)
    
    def nro_de_documento(self, obj):
        return f'{obj.origen}-{obj.cedula}'
    nro_de_documento.short_description = 'Nro. Documento'