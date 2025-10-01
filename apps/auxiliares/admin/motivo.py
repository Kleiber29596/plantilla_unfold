from django.contrib import admin
from apps.auxiliares.models.motivo import Motivo

@admin.register(Motivo)
class MotivoAdmin(admin.ModelAdmin):
    list_display = ("descripcion",)