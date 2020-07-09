from django.urls import path, re_path
from django.conf.urls import url,include
from . import views
urlpatterns = [
    path('<domain>',views.index),
    path('login/<domain>',views.login),
    path('programme/<auth>/<domain>',views.programmes),
    path('profile/<auth>/<domain>',views.profile),
    path('messages/<auth>/<domain>',views.messages),    
]