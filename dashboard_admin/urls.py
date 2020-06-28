from django.urls import path, re_path,include

from django.views.generic import TemplateView
from .views import auth_form,auth_request,del_auth,_dashboard,_status

urlpatterns = [
    path("",auth_form),
    path("login",auth_form,name="official_login"),
    path("logout",del_auth,name="official_logout"),
    path("auth",auth_request),
    #dashboard
    path("dashboard/",include([
        path("home/",_dashboard.index),
        path("",_dashboard.index,name=''),
    ])),
    #status
    path("status/",include([
        path("home/",_status.index),
        path("",_status.index),
    ])),



    ##re_path('happy', TemplateView.as_view(template_name="app/index.html"))
]