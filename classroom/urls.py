from django.conf.urls import url, include

from django.urls import path, re_path
from . import views
from .forms import UserLoginForm

from django.contrib.auth import views as auth_django

from .views import home_view, signup_view,payment_check

urlpatterns = [
    path('login/',
        auth_django.LoginView.as_view(authentication_form=UserLoginForm,template_name = 'custom_login.html'),
        name='fghfgh'
    ),
    path(
        'logout/',
        auth_django.LogoutView.as_view(template_name = 'custom_exit.html'),
        name='fghfghjgh'
    ),
    path(
        'pwd/',
        auth_django.PasswordChangeView.as_view(),
        name='fghfghjgh'
    ),
    
    path('profile/', home_view, name="home"),
    path('', home_view, name="home"),
    path('', home_view, name="home"),
    path('signup/', signup_view, name="signup"),
    path('order_payment_validate/', payment_check),
]

