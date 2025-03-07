"""eduzone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.conf.urls import url,include
from django.views.static import serve 
from django.views.generic import TemplateView
from classroom.views import app
from studentsonly.views import index as mainpage,service,service2
from django.shortcuts import redirect
def smaasred(request):
    return redirect('/')

urlpatterns = [
    path('_infox/', admin.site.urls),
    path('_accounts/',include('classroom.urls')),
    path('console/',include('diya_api.urls')),
    path('_pay/',include('edupay.urls')),
    path('_admin/',include('dashboard_admin.urls')),
    url(r'^manifest.json',mainpage),
    url(r'^site.webmanifest',mainpage),
    url(r'^service-worker.js',service),
    path(r'precache-manifest.<query>.js',service2),
    #url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    #url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
    url(r'index.html',app),
    url(r'^channel', app),
    url(r'^channel/(?P<path>.*)$', app),
    url(r'^$',app),
]
#urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
