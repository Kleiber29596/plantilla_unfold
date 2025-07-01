from django.contrib import admin
from apps.gestion.models.inventario import Inventario
from django.utils.html import format_html  # Importa format_html correctamente
from import_export.admin                                    import ExportMixin
from import_export                                          import resources
from import_export.fields                                   import Field



class InventarioResource(resources.ModelResource):
   
    class Meta:
        model = Inventario
        fields = ['descripcion', 'cod_catalogo', 'cod_bien', 'valor_unitario', 'unidad_usuaria', 'responsable']
        export_order = ['descripcion', 'cod_catalogo', 'cod_bien', 'valor_unitario', 'unidad_usuaria', 'responsable']
        exclude = ['id']


    def dehydrate_descripcion(self, obj):
        return f"{obj.descripcion.categoria} {obj.descripcion.modelo} {obj.descripcion.descripcion}" 

    def dehydrate_unidad_usuaria(self, obj):
        return obj.unidad_usuaria.descripcion 

    def dehydrate_responsable(self, obj):
        return f"{obj.responsable.nombres_apellidos}" 


def estado(obj):
    return format_html('<span class="badge rounded-pill text-bg-success">{}</span>', obj.estado)


@admin.register(Inventario)
class InventarioAdmin(ExportMixin, admin.ModelAdmin):
    list_display        = ("descripcion", "cod_bien",  "tipo_uso", "responsable","ubicacion", estado)
    list_filter         = ("tipo_uso", "estado", "responsable","ubicacion","cod_bien")
    resource_class      = InventarioResource

