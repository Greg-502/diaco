from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import *

urlpatterns = [
    path('',  Main.as_view(), name="main"),
    path('data/',  login_required(Data.as_view()), name="data"),
]