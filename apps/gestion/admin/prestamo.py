from django.contrib               import  admin
from apps.gestion.models.prestamo import  Prestamo, DetallePrestamo



class DetallePrestamoInline(admin.TabularInline):
    model = DetallePrestamo
    extra = 0
    can_delete = False
    show_change_link = True

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = (
        "fecha_inicio",
        "fecha_final",
        "fecha_devolucion",
        "status",
    )
    list_filter = ("status", "fecha_inicio", "fecha_final")
    search_fields = ("bien__codigo", "bien__descripcion", "motivo")
    date_hierarchy = "fecha_inicio"
    ordering = ("-fecha_inicio",)
    inlines = [DetallePrestamoInline]

    fieldsets = (
        ("Información del Préstamo", {
            "fields": ("fecha_inicio", "fecha_final", "motivo")
        }),
        # ("Contrato", {
        #     "fields": ("contrato_digital", "contrato_fisico"),
        #     "classes": ("collapse",),  # Se puede ocultar para que no moleste
        # }),
        ("Devolución", {
            "fields": ("fecha_devolucion", "status"),
        })
    )

    readonly_fields = ("creado", "actualizado")

    # def get_queryset(self, request):
    #     """Optimiza la carga en el admin con select_related."""
    #     qs = super().get_queryset(request)
    #     return qs.select_related("bien")
