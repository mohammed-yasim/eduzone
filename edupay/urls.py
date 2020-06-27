from django.urls import path, re_path
from django.conf.urls import url,include
from . import views
from classroom.views import makeOrder


urlpatterns = [
    url('^$',views.index),
    path('makeorder',makeOrder)
]