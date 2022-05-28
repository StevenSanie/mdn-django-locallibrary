from os import stat
from django import urls
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('catalog.urls')),
    path('accounts/', include('django.contrib.auth.urls')),     
]

urlpatterns += [
    path('', RedirectView.as_view(url='catalog/', permanent=True))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 