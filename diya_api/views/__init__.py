from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import re
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime,timedelta
from django.http import JsonResponse
from django.core import serializers
from diya_api.models import Channel,Programme,Playlist,Client
import json
import ast 
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from diya_api.serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

@csrf_exempt
def channels(request):
    start = datetime.now().timestamp() * 1000
    json_template = {'response': 1,'status': 'success','message':'','data':[]}
    queryset = Channel.objects.all()
    if(queryset.count() >= 1):
        var_list="["
        for channel in queryset:
            var_list+="{"
            var_list+=" 'name':'%s', " %(channel.name)
            var_list+=" 'icon':'%s',"%(channel.icon)
            var_list+=" 'info':'%s',"%(channel.info)
            var_list+=" 'uri':'%s',"%(channel.uri)
            var_list+="},"
        var_list+="]"
        res = ast.literal_eval(var_list) 
        json_template['data'] = res
        loadingpagetime = datetime.now().timestamp() * 1000 - start
        print(loadingpagetime)
        return HttpResponse(json.dumps(json_template), content_type="text/json-comment-filtered")
    return JsonResponse(json_template)
@csrf_exempt
def channel(request,name):
    start = datetime.now().timestamp() * 1000
    json_template = {'response': 1,'status': 'success','message':'','data':{}}
    q_channel = Channel.objects.get(uri=name)
    json_template['data']['name'] = q_channel.name
    queryset = Programme.objects.filter(channel=q_channel)
    if(queryset.count() >= 1):
        post_liste = serializers.serialize('json', queryset)
        var_list = []
        for data in json.loads(post_liste):
            var_list.append(data['fields'])
        json_template['data']['programmes'] = var_list
        loadingpagetime = datetime.now().timestamp() * 1000 - start
        print(loadingpagetime)
        return HttpResponse(json.dumps(json_template), content_type="text/json-comment-filtered")
        
    return JsonResponse(json_template)

@csrf_exempt
def programme(request,name,pgm):
    json_template = {'response': 1,'status': 'success','message':''}
    q_channel = Channel.objects.get(uri=name)
    q_programm = Programme.objects.get(uri=pgm,channel=q_channel)
    enddate = datetime.now()
    queryset = Playlist.objects.filter(programme=q_programm)
    if(queryset.count() >= 1):
        var_list="["
        for aa in queryset:
            var_list+="{"
            var_list+=" 'name':'%s', " %(aa.name)
            var_list+=" 'icon':'%s',"%(aa.name)
            var_list+=" 'playlist':[ "
            for video in aa.video.all():
                if(video.date < datetime.now()):
                    var_list+="{"
                    var_list+=" 'name':'%s'," %(video.name)
                    var_list+=" 'info':'%s'," %(video.info)
                    var_list+=" 'icon':'%s'," %(video.icon)
                    var_list+=" 'date':'%s'," %(video.date)
                    var_list+=" 'uri':'%s'," %(video.uri)
                    var_list+="},"
            var_list+="]"
            var_list+="},"
        var_list+="]"
        res = ast.literal_eval(var_list) 
        json_template['data'] = res
        return HttpResponse(json.dumps(json_template), content_type="text/json-comment-filtered")
    return JsonResponse(json_template)