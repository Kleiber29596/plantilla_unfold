from django.contrib import admin
from ..models import Devolucion, DetalleDevolucion

class DetalleDevolucionInline(admin.TabularInline):
    model = DetalleDevolucion
    extra = 1

@admin.register(Devolucion)
class DevolucionAdmin(admin.ModelAdmin):
    list_display = ('id', 'asignacion', 'fecha_devolucion')
    list_filter = ('fecha_devolucion',)
    search_fields = ('asignacion__id',)
    inlines = [DetalleDevolucionInline]
