import threading
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# from django.contrib.messages.views import SuccessMessageMixin

def create_mail(email, subject, template_path, context):
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

def send_welcome_mail(request):
    welcome_mail = create_mail(
        request,
        'Prueba de envio de correo',
        'emails/buy.html',
        {
            'username': request
        }
    )

    welcome_mail.send(fail_silently = False)

def send_mail(request):
    thread = threading.Thread(
        target = send_welcome_mail(request),
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
