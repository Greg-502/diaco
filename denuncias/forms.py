from django import forms
from django.forms.forms import Form
from django.forms.models import ModelChoiceField
from .models import *

class FormQueja(Form):
    departamento = ModelChoiceField(queryset=Departamentos.objects.all(), empty_label='Departamentos *')
    municipio = ModelChoiceField(queryset=Municipios.objects.none(), empty_label='Municipios *')
    negocio = ModelChoiceField(queryset=Negocios.objects.none(), empty_label='Negocios *')
    sucursal = ModelChoiceField(queryset=Sucursales.objects.none(), empty_label='Sucursales *')
    queja = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder':'Describa su queja *', 'id':'summernote'}))

    newnegocio = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Nombre del negocio *', 'id': 'inputNegocio', 'autofocus':True}), required=True)
    allnegocios = ModelChoiceField(queryset=Negocios.objects.none(), empty_label='Negocios *')
    newsucursal = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Referencia o ubicación *', 'id': 'inputSucursal'}), required=True)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
            form.field.widget.attrs['required'] = True 