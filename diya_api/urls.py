from django.urls import path, re_path
from django.conf.urls import url,include
from .views import channel,channels,programme,UserViewSet,GroupViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    path("channels",channels),
    path("channel/<name>",channel),
    path("<name>/programme/<pgm>",programme),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]