from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from django.conf.urls import handler404
# from denuncias.views import page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('denuncias.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.STATIC_URL)

# handler404 = page_not_found