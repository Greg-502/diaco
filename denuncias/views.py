from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.list import ListView
from django.db import connection
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
                for i in Negocios.objects.raw('call getNegocio(%s)', [request.POST['id']]):
                    data.append({'pk': i.pk, 'nego': i.nombre})
            elif action == 'sucurs':
                data = []
                for i in Sucursales.objects.raw('call getSucursales(%s, %s)', [request.POST['id_mun'], request.POST['id']]):
                    data.append({'pk': i.pk, 'sucrs': i.ubicacion})
            elif action == 'crqueja':
                cursor = connection.cursor()
                cursor.execute('call spInsertQueja(%s, %s)', [request.POST['razon'], request.POST['tienda']] )
            elif action == 'allneg':
                data = []
                for i in Negocios.objects.raw('call getAllNeg'):
                    data.append({'pk': i.pk, 'all': i.nombre})
            elif action == 'addCom':
                cursor = connection.cursor()
                cursor.execute('call spInsertNegocio(%s)', [request.POST['inputNegocio']])
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
            data = Quejas.objects.get(pk=request.POST['id']).toJSON()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_queryset(self):
        return self.model.objects.filter(estado = True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Quejas'
        context['quejas'] = self.get_queryset()
        return context