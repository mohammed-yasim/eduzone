from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import TemplateView
from .views import restart,pull,index,collectstatic


from django.contrib.auth import views as auth_django



from infox_controller.forms import UserLoginForm

urlpatterns = [
    path('django/', admin.site.urls),
    path('restart',restart),
    path('collectstatic',collectstatic),
    path('pull',pull),
    path('',index),
    path(
        'login/',
        auth_django.LoginView.as_view(
            template_name="system_index.html",
            authentication_form=UserLoginForm
            ),
        name='infox_login'
)
]