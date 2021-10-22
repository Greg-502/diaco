from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import path
from .views import *

urlpatterns = [
    path('',  Main.as_view(), name="main"),
    path('data/', login_required(Data.as_view()), name="data"),
    path('accounts/login/', LoginView.as_view(template_name='registration/login.html', redirect_authenticated_user=True), name="login"),
]