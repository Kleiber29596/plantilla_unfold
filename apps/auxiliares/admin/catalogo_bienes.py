from django.contrib import admin
from ..models import  Estado, CondicionBien, Color, Marca, Modelo, TipoBien
from unfold.admin import ModelAdmin, TabularInline

class ModeloInline(TabularInline):
    model = Modelo
    extra = 1


class AdminMarca(ModelAdmin):
    search_fields = ('nombre',)
    inlines = [ModeloInline]


class AdminModelo(ModelAdmin):
    search_fields = ('nombre',)

class AdminTipoBien(ModelAdmin):
    search_fields = ('nombre',)

class AdminColor(ModelAdmin):
    search_fields = ('nombre',)

class AdminCondicionBien(ModelAdmin):
    search_fields = ('nombre',)

admin.site.register(Estado, ModelAdmin)
admin.site.register(CondicionBien, AdminCondicionBien)
admin.site.register(Color, AdminColor)
admin.site.register(Marca, AdminMarca)
admin.site.register(Modelo, AdminModelo)
admin.site.register(TipoBien, AdminTipoBien)
