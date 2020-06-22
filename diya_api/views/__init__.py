from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import re
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime,timedelta
from django.http import JsonResponse
from django.core import serializers
from diya_api.models import Channel,Programme,Playlist,Client,Categories
import json
import ast 

@csrf_exempt
def channels(request):
    start = datetime.now().timestamp() * 1000
    json_template = {'response': 0,'status': 'fail','message':'Please Login','data':[],'catfilter':[]}
    if request.user:#.is_authenticated
        json_template = {'response': 200,'status': 'success','message':'','data':[],'catfilter':[]}
        filterset = Categories.objects.all()
        if (filterset.count() >= 1):
            filter_list = "["
            for filters in filterset:
                filter_list+= "{"
                filter_list+= " 'name':'%s', "%(filters.name)
                filter_list+= " 'uri':'%s', "%(filters.uri)
                filter_list+= "},"
            filter_list+= "]"
            filter_listres = ast.literal_eval(filter_list) 
            json_template['catfilter'] = filter_listres
        queryset = Channel.objects.filter(pub=True,active=True)
        if(queryset.count() >= 1):
            var_list="["
            for channel in queryset:
                var_list+="{"
                var_list+=" 'name':'%s', " %(channel.name)
                var_list+=" 'icon':'%s',"%(channel.icon)
                var_list+=" 'info':'%s',"%(channel.info)
                var_list+=" 'uri':'%s',"%(channel.uri)
                var_list+=" 'category':'%s',"%(channel.category.uri)
                var_list+="},"
            var_list+="]"
            res = ast.literal_eval(var_list) 
            json_template['data'] = res
            loadingpagetime = datetime.now().timestamp() * 1000 - start
            print(loadingpagetime)
    return HttpResponse(json.dumps(json_template), content_type="application/json")

@csrf_exempt
def channel(request,name):
    start = datetime.now().timestamp() * 1000
    json_template = {'response': 200,'status': 'OK','message':'','data':{}}
    try:
        q_channel = Channel.objects.get(uri=name)
        json_template['data']['name'] = q_channel.name
        if(q_channel.icon):
            json_template['data']['icon'] = "%s" %(q_channel.icon)
    
        json_template['data']['uri'] = q_channel.uri
        json_template['data']['programmes'] = []
        try:
            queryset = Programme.objects.filter(channel=q_channel)
            if(queryset.count() >= 1):
                post_liste = serializers.serialize('json', queryset)
                var_list = []
                for data in json.loads(post_liste):
                    var_list.append(data['fields'])
                    json_template['data']['programmes'] = var_list
                loadingpagetime = datetime.now().timestamp() * 1000 - start
                print(loadingpagetime)
        except:
            pass
        return HttpResponse(json.dumps(json_template), content_type="application/json")
    except Exception  as e:
        json_template['response'] = 404
        json_template['status'] = 'Not Data Found'
        json_template['message'] = '%s'%(e)
    return HttpResponse(json.dumps(json_template), content_type="application/json")

@csrf_exempt
def programme(request,name,pgm):
    json_template = {'response': 1,'status': 'success','message':'','data':[]}
    q_channel = Channel.objects.get(uri=name)
    q_programm = Programme.objects.get(uri=pgm,channel=q_channel)
    enddate = datetime.now()
    queryset = Playlist.objects.filter(programme=q_programm)
    if(queryset.count() >= 1 and q_programm.premium==True):
        json_template['demo'] = True
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
                    if(video.demo==True):
                        var_list+=" 'uri':'%s'," %(video.uri)
                    else:
                        var_list+=" 'uri':'%s'," %("/pay")
                    var_list+=" 'demo':'%s'," %(video.demo)
                    var_list+="},"
            var_list+="]"
            var_list+="},"
        var_list+="]"
        res = ast.literal_eval(var_list) 
        json_template['data'] = res
        return HttpResponse(json.dumps(json_template), content_type="application/json")
    if(queryset.count() >= 1 and q_programm.premium==False):
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
        return HttpResponse(json.dumps(json_template), content_type="application/json")
    return JsonResponse(json_template)