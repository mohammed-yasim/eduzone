from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import re
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.core import serializers
from diya_api.models import Channel, Programme, Playlist, Client, Categories,Video
import json
import ast
from classroom.models import SubscriptionList as SList
from dashboard_admin.models import Esubscibers,Replies,Comment,Article


def bypass(request):
    #user = authenticate(username='yasim', password='yasim007')
    #login(request, user)
    return True

@csrf_exempt
def videoArticles(request,vid):
    return 0

@csrf_exempt
def channels(request):
    bypass(request)
    start = datetime.now().timestamp() * 1000
    json_template = {'response': 0, 'status': 'fail',
                     'message': 'Please Login', 'data': [], 'catfilter': []}
    if request.user.is_authenticated:
        json_template = {'response': 200, 'status': 'success',
                         'message': '', 'data': [], 'catfilter': []}
        filterset = Categories.objects.values_list('name','uri', named=True)
        if (filterset.count() >= 1):
            filter_list = """["""
            for filters in filterset:
                filter_list += """{"""
                filter_list += """ "name":"%s", """ % (filters.name)
                filter_list += """ "uri":"%s", """ % (filters.uri)
                filter_list += """},"""
            filter_list += """]"""
            filter_listres = ast.literal_eval(filter_list)
            json_template['catfilter'] = filter_listres
        queryset = Channel.objects.filter(pub=True,active=True)
        if(queryset.count() >= 1):
            var_list = """["""
            for channel in queryset:
                var_list += """{"""
                var_list += """ "name":"%s", """ % (channel.name)
                var_list += """ "icon":"%s",""" % (channel.icon)
                var_list += """ "info":"%s",""" % (channel.info)
                var_list += """ "uri":"%s",""" % (channel.uri)
                var_list += """ "category":"%s",""" % (channel.category.uri)
                var_list += """},"""
            var_list += """]"""
            res = ast.literal_eval(var_list)
            json_template['data'] = res
            loadingpagetime = datetime.now().timestamp() * 1000 - start
            print(loadingpagetime)
    return HttpResponse(json.dumps(json_template), content_type="application/json")


@csrf_exempt
def channel(request, name):
    bypass(request)
    json_template = {'response': 0, 'status': 'Not Ok',
                     'message': 'Please Login', 'data': {}}
    if request.user.is_authenticated:
        start = datetime.now().timestamp() * 1000
        json_template = {'response': 200,
                         'status': 'OK', 'message': '', 'data': {}}
        try:
            q_channel = Channel.objects.get(uri=name,pub=True,active=True)
            # print(q_channel.programme.all())
            json_template['data']['name'] = q_channel.name
            if(q_channel.icon):
                json_template['data']['icon'] = "%s" % (q_channel.icon)
            json_template['data']['uri'] = q_channel.uri
            json_template['data']['info'] = q_channel.info
            json_template['data']['programmes'] = []
            try:
                # Programme.objects.filter(channel=q_channel)
                queryset = q_channel.programme.all()
                if(queryset.count() >= 1):
                    post_liste = serializers.serialize('json', queryset)
                    var_list = []
                    for data in json.loads(post_liste):
                        var_list.append(data['fields'])
                    json_template['data']['programmes'] = var_list
            except:
                pass
            loadingpagetime = datetime.now().timestamp() * 1000 - start
            print(loadingpagetime)
            return HttpResponse(json.dumps(json_template), content_type="application/json")
        except Exception as e:
            json_template['response'] = 404
            json_template['status'] = 'Not Data Found'
            json_template['message'] = '%s' % (e)
        return HttpResponse(json.dumps(json_template), content_type="application/json")
    else:
        return HttpResponse(json.dumps(json_template), content_type="application/json")


@csrf_exempt
def programme(request, name, pgm):
    bypass(request)
    json_template = {'response': 0, 'status': 'Not Ok',
                     'message': 'Please Login', 'data': []}
    try:
        if request.user.is_authenticated:
            json_template = {'response': 200,
                             'status': 'OK', 'message': '', 'data': []}
            q_channel = Channel.objects.get(uri=name)
            q_programm = Programme.objects.get(uri=pgm, channel=q_channel)
            enddate = datetime.now()
            queryset = Playlist.objects.filter(programme=q_programm)
            purchased = False
            try:
                activators = SList.objects.get(
                    programme=q_programm, user=request.user, is_activated=True)
                expiry = activators.date + timedelta(days=activators.validity)
                if datetime.now() <= expiry:
                    purchased = True
                else:
                    purchased = False
            except Exception as e:
                print(e)
                purchased = False
            if(queryset.count() >= 1 and q_programm.premium == True and purchased == False):
                start = datetime.now().timestamp() * 1000
                json_template['demo'] = True
                var_list = """["""
                width = 0
                for aa in queryset:
                    var_list += """{"""
                    var_list += """ "name":"%s", """ % (aa.name)
                    var_list += """ "playlist":[ """
                    count_width = 0
                    pagit = 1
                    pagit = int(request.GET["p"])
                    for video in aa.video.filter(deleted=False,banned=False).extra(where=['date<%s'], params=[datetime.now()]).order_by('-date')[pagit*10-10:pagit*10]:
                        count_width += 1
                        var_list += """{"""
                        var_list += """ "name":"%s",""" % (video.name)
                        var_list += """ "uid":"%s",""" % (video.uid)
                        var_list += """ "info":"%s",""" % (video.info)
                        var_list += """ "icon":"%s",""" % (video.icon)
                        var_list += """ "date":"%s",""" % (video.date)
                        if(video.demo == True):
                            var_list += """ "uri":"%s",""" % (video.uri)
                        else:
                            var_list += """ "uri":"/_pay?p=%s",""" % (
                                q_programm.uid)
                        var_list += """ "demo":"%s",""" % (video.demo)
                        var_list += """},"""
                    if count_width > width:
                        width = count_width
                    var_list += """]"""
                    var_list += """},"""
                print("final : ", width)
                var_list += """]"""
                res = ast.literal_eval(var_list)
                json_template['data'] = res
                json_template['width'] = width
                loadingpagetime = datetime.now().timestamp() * 1000 - start
                print(loadingpagetime)
                return HttpResponse(json.dumps(json_template), content_type="application/json")
            elif((queryset.count() >= 1 and q_programm.premium == False) or (queryset.count() >= 1 and purchased == True)):
                var_list = """["""
                width = 0
                for aa in queryset:
                    var_list += """{"""
                    var_list += """ "name":"%s", """ % (aa.name)
                    var_list += """ "playlist":[ """
                    count_width = 0
                    pagit = 1
                    pagit = int(request.GET["p"])
                    for video in aa.video.filter(deleted=False,banned=False).extra(where=['date<%s'], params=[datetime.now()]).order_by('-date')[pagit*10-10:pagit*10]:
                        count_width += 1
                        var_list += """{"""
                        var_list += """ "name":"%s",""" % (video.name)
                        var_list += """ "uid":"%s",""" % (video.uid)
                        var_list += """ "info":"%s",""" % (video.info)
                        var_list += """ "icon":"%s",""" % (video.icon)
                        var_list += """ "date":"%s",""" % (video.date)
                        var_list += """ "uri":"%s",""" % (video.uri)
                        var_list += """},"""
                    if count_width > width:
                        width = count_width
                    var_list += """]"""
                    var_list += """},"""
                var_list += """]"""
                res = ast.literal_eval(var_list)
                json_template['data'] = res
                json_template['width'] = width
                return HttpResponse(json.dumps(json_template), content_type="application/json")
            else:
                json_template['response'] = 404
                json_template['status'] = 'Not OK'
                json_template['message'] = 'Not Data in this Programme'
                return HttpResponse(json.dumps(json_template), content_type="application/json")
        else:
            return HttpResponse(json.dumps(json_template), content_type="application/json")

    except Exception as e:
        json_template['response'] = 404
        json_template['status'] = 'Not OK'
        json_template['message'] = '%s' % (e)
        return HttpResponse(json.dumps(json_template), content_type="application/json")

def videoArticles(request,vid):
    bypass(request)
    start = datetime.now().timestamp() * 1000
    json_template = {'response': 0, 'status': 'fail',
                     'message': 'Please Login', 'data': {}}
    json_template['data']['vid'] = vid
    video = Video.objects.get(uid=vid)
    json_template['data']['name'] = video.name
    json_template['data']['info'] = video.info
    try:
        article = Article.objects.get(uid=vid)
        json_template['data']['content'] = article.text
        json_template['data']['article'] = True
    except:
        json_template['data']['article'] = False
   
    return HttpResponse(json.dumps(json_template), content_type="application/json")

