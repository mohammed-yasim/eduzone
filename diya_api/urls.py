from django.urls import path, re_path
from django.conf.urls import url,include
from .views import channel,channels,programme,videoArticles



urlpatterns = [
    path("channels",channels),
    path("channel/<name>",channel),
    path("<name>/programme/<pgm>",programme),
    path("article/<vid>",videoArticles),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]