from django.http import request
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from datetime import datetime
from django.db import connection
from django.shortcuts import render
from .models import *
from .forms import *

class Main(TemplateView):
    template_name = 'index.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'munis':
                data = []
                for i in Municipios.objects.filter(departamento = request.POST['id']):
                    data.append({'pk': i.pk, 'muni': i.nombre_mun})
            elif action == 'negos':
                data = []
                for i in Negocios.objects.raw("call getNegocio("+'%s'+")", [request.POST['id']]):
                    data.append({'pk': i.pk, 'nego': i.nombre})
            elif action == 'sucurs':
                data = []
                for i in Sucursales.objects.raw("call getSucursales("+'%s'+","+'%s'+")", [request.POST['id_mun'], request.POST['id']]):
                    data.append({'pk': i.pk, 'sucrs': i.ubicacion})
            elif action == 'crqueja':
                actual = datetime.now()
                cursor = connection.cursor()
                cursor.execute("call spInsertQueja("+'%s'+","+'%s'+","+'%s'+")", [request.POST['razon'], actual, request.POST['tienda']] )
            elif action == 'allneg':
                data = []
                for i in Negocios.objects.raw('call getAllNeg'):
                    data.append({'pk': i.pk, 'all': i.nombre})
            elif action == 'addCom':
                cursor = connection.cursor()
                cursor.execute("call spInsertNegocio("+'%s'+")", [request.POST['inputNegocio']])
            elif action == 'addScr':
                cursor = connection.cursor()
                cursor.execute('call spInsertSucursal(%s,%s,%s)', [request.POST['inputSuc'], request.POST['idMux'], request.POST['idAll']])
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Denuncias'
        context['form'] = FormQueja
        return context

class Data(ListView):
    model = Quejas
    template_name = 'data.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == '1':
                data = []
                data = Quejas.objects.get(pk=request.POST['id']).toJSON()
            elif action == 'count':
                data = []
                quejas = Quejas.objects.count()
                data.append(quejas)
            elif action == 'radial':
                data = []
                for i in Regiones.objects.raw('call spXregiones'):
                    data.append({'totales': i.totales, 'regiones': i.regiones})
            elif action == 'pie':
                data = []
                for i in Negocios.objects.raw('call spXnegocios'):
                    data.append({'totales': i.totales, 'negocios': i.negocios})
            elif action == 'barra':
                data = []
                for i in Departamentos.objects.raw('call spXDeptos'):
                    data.append({'totales': i.totales, 'deptos': i.deptos})
            elif action == 'lineal':
                data = []
                for i in Quejas.objects.raw('call spXfechas'):
                    data.append({'totales':i.totales, 'creado':i.creado})
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Quejas'
        context['quejas'] = self.get_queryset()
        return context

def handler404(request, exception):
    return render(request, '404.html')