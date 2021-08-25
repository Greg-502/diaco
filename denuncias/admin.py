from django.contrib import admin
from .models import *

class MunAdmin(admin.ModelAdmin):
    list_per_page = 10

@admin.register(Quejas)
class QuejasAdmin(admin.ModelAdmin):
    list_display = ('pk', 'estado', 'creacion')
    list_editable = ('estado',)


@admin.register(Departamentos)
class RegionesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'nombre_dep', 'region',)

    search_fields = (
        'region__nombre_reg',
    )

    list_filter = (
        'region__nombre_reg',
    )

admin.site.register(Regiones)
admin.site.register(Municipios, MunAdmin)
admin.site.register(Negocios)
admin.site.register(Sucursales)
