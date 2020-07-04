from django.urls import path, re_path,include

from django.views.generic import TemplateView
from .views import auth_form,auth_request,del_auth,_dashboard,_status,_videos,_channels,_subscribers

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
    #subscribers
    path("subscribers/",include([
         path("",_subscribers.index),
         path("add",_subscribers.addser),
    ])),
    #videos
    path("videos/",include([
        path("home/",_videos.index),
        path("",_videos.index),
        path("edit/<vid>",_videos.editvideo),
        path("comments",_videos.comments),
    ])),
    #channels
    path("channels/",include([
        path("all/",_channels.index),
        path("",_channels.index),
        path("programmes/<qchannel>",_channels.allprogrammes),
        path("programmes/<qchannel>/playlist/<qprogramme>",_channels.allplaylist),
        path("programmes/<qchannel>/playlist/<qprogramme>/videos/<qplaylist>",_channels.videos),
    ])),



    ##re_path('happy', TemplateView.as_view(template_name="app/index.html"))
]