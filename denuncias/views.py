from django.http.response import HttpResponse, JsonResponse
from django.views.generic import ListView, TemplateView
import pytz
from datetime import datetime
from django.db import connection
from .send_mail import send_mail
from .models import *
from .forms import *

class Main(TemplateView):
    template_name = 'index.html'

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
                try:
                    timezone = pytz.timezone('America/Guatemala')
                    actual = datetime.now(timezone)
                    cursor = connection.cursor()
                    cursor.execute("call spInsertQueja("+'%s'+","+'%s'+","+'%s'+")", [request.POST['razon'], actual, request.POST['tienda']] )
                    
                    email_to = request.POST['email']
                    send_mail(email_to)
                except Exception as e:
                    print(e)
                    return False
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
            elif action == 'search':
                data = []
                try:
                    for i in Quejas.objects.raw('call spSearching('+"%s"+')', [request.POST['id']]):
                        data.append({'estado': i.estado, 'creacion': i.creacion, 'municipio': i.municipio, 'negocio': i.negocio})
                    # data = Quejas.objects.get(pk=request.POST['id']).toSearch()
                except Exception as e:
                    return HttpResponse(e)
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

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == '1':
                data = []
                data = Quejas.objects.get(pk=request.POST['id']).toJSON()
            elif action == 'count':
                data = []
                quejas = Quejas.objects.filter(estado = True).count()
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
            elif action == 'remove':
                cursor = connection.cursor()
                cursor.execute("call spUpdateQueja("+'%s'+")", [request.POST['id']])
            elif action == 'mapas':
                data = []
                for i in Quejas.objects.raw('call spXmapa'):
                    data.append({'mapa': i.mapa, 'totales':i.totales})
            elif action == 'search':
                data = []
                try:
                    for i in Quejas.objects.raw('call spSearching('+"%s"+')', [request.POST['id']]):
                        data.append({'estado': i.estado, 'creacion': i.creacion, 'municipio': i.municipio, 'negocio': i.negocio})
                except Exception as e:
                    return HttpResponse(e)
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    # def mapas(self):
    #     data = []
    #     for i in Quejas.objects.raw('call spXmapa'):
    #         data.append({'mapa': i.mapa, 'totales':i.totales})
    #     return data

    def get_queryset(self):
        return self.model.objects.filter(estado = True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Quejas'
        context['quejas'] = self.get_queryset()
        return context

# def page_not_found(request, exception):
#     return render(request, '404.html')