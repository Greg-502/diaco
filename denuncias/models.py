from django.db import models
from django.db.models.deletion import PROTECT
from datetime import datetime

from django.forms.models import model_to_dict

class Regiones(models.Model):
    nombre_reg = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre_reg

    class Meta:
        verbose_name = "Región"
        verbose_name_plural = "Regiones"
        ordering = ['nombre_reg']

class Departamentos(models.Model):
    nombre_dep = models.CharField(max_length=100, unique=True)
    region = models.ForeignKey(Regiones, on_delete=PROTECT)
    mapa = models.CharField(max_length=10, unique=True)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def __str__(self):
        return self.nombre_dep

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        ordering = ['nombre_dep']

class Municipios(models.Model):
    nombre_mun = models.CharField(max_length=100, unique=False)
    departamento = models.ForeignKey(Departamentos, on_delete=PROTECT)

    def __str__(self):
        return self.nombre_mun

    class Meta:
        verbose_name = "Municipio"
        verbose_name_plural = "Municipios"
        ordering = ['nombre_mun']

class Negocios(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "negocio"
        verbose_name_plural = "negocios"
        ordering = ['nombre']

class Sucursales(models.Model):
    ubicacion = models.CharField(max_length=100, unique=False)
    negocio = models.ForeignKey(Negocios, on_delete=PROTECT)
    municipio = models.ForeignKey(Municipios, on_delete=PROTECT)

    def __str__(self):
        return self.ubicacion

    class Meta:
        verbose_name = "Sucursal"
        verbose_name_plural = "Sucursales"
        ordering = ['ubicacion']

class Quejas(models.Model):
    queja = models.TextField()
    estado = models.BooleanField(default=True)
    creacion = models.DateTimeField(default=datetime.now())
    sucursal = models.ForeignKey(Sucursales, on_delete=PROTECT)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def __str__(self):
        return self.queja

    class Meta:
        verbose_name = "Queja"
        verbose_name_plural = "Quejas"