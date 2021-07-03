import threading
from django.core import serializers
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.http.response import HttpResponse, JsonResponse
# from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView
# from django.contrib.messages.views import SuccessMessageMixin
from datetime import datetime
from django.db import connection
from django.shortcuts import redirect, render
from django.conf import settings
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
                    actual = datetime.now()
                    cursor = connection.cursor()
                    cursor.execute("call spInsertQueja("+'%s'+","+'%s'+","+'%s'+")", [request.POST['razon'], actual, request.POST['tienda']] )

                    email_to = request.POST['email']
                    self.send_mail(email_to)
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
                    data = Quejas.objects.get(pk=request.POST['id']).toSearch()
                except Exception as e:
                    return HttpResponse(e)
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def create_mail(self, email, subject, template_path, context):
        template = get_template(template_path)
        content = template.render(context)

        mail = EmailMultiAlternatives(
            subject = subject,
            body = '',
            from_email = settings.EMAIL_HOST_USER,
            to = [
                email
            ],
            cc=[]
        )
        mail.attach_alternative(content, 'text/html')
        return mail

    def send_welcome_mail(self, request):
        welcome_mail = self.create_mail(
            'gp.israel@icloud.com',
            'Prueba de envio de correo',
            'emails/buy.html',
            {
                'username': request
            }
        )

        welcome_mail.send(fail_silently = False)

    def send_mail(self, request):
        thread = threading.Thread(
            target = self.send_welcome_mail(request),
            args=(request,)
        )

        thread.start()
        return True

        # try:
        #     email_to = email
        #     mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        #     mailServer.ehlo()
        #     mailServer.starttls()
        #     mailServer.ehlo()
        #     mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

        #     mensaje = MIMEMultipart()
        #     mensaje['From']=settings.EMAIL_HOST_USER
        #     mensaje['To']=email_to
        #     mensaje['Subject']="Tienes un correo"

        #     content = render_to_string('emails/buy.html', {'username': 'Greg Puac'})
        #     mensaje.attach(MIMEText(content, 'html'))

        #     mailServer.sendmail(settings.EMAIL_HOST_USER, email_to, mensaje.as_string())
        #     print('Enviado...')

        #     return True
        # except Exception as e:
        #     print(e)

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