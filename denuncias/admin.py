from django.contrib import admin
from .models import *

class MunAdmin(admin.ModelAdmin):
    list_per_page = 10

admin.site.register(Regiones)
admin.site.register(Departamentos)
admin.site.register(Municipios, MunAdmin)
admin.site.register(Negocios)
admin.site.register(Sucursales)
admin.site.register(Quejas)
