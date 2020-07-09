from django.shortcuts import render, HttpResponse
from diya_api.models import Channel,Esubscibers,Elogin
import json,ast
from datetime import datetime
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from uuid import uuid4
from datetime import datetime

def index(request, domain):
    data = {'response':0,'status':'Not OK','message':''}
    try:
        channel = Channel.objects.get(e_host=domain,enterprize=True)
        data['channel'] = channel.name
        data['info'] = channel.info
        data['auth'] = '%s'%(uuid4().hex)
        data['response'] = 200
        data['status'] = 'OK'
    except Exception as e:
        data['response'] = 404
        data['message'] = '%s'%(e)
    return HttpResponse(json.dumps(data), content_type="application/json")


from django.contrib.auth.hashers import make_password
@csrf_exempt
def login(request,domain):
    data = {'response':0,'status':'Not OK','message':''}
    try:
        username = request.POST['uname']
        password = request.POST['paswd']
        cookie = request.POST['cookie']
        channel = Channel.objects.get(e_host=domain,enterprize=True)
        user = Esubscibers.objects.get(username=username,password=password,client=channel.who)
        if(user):
            auth = '%s'%(uuid4().hex)
            data['auth'] = auth
            #print("Hashed password is:", make_password(auth))
            data['key'] = make_password(auth)
            data['token'] = "%s"%(hash(auth))
            user.auth = auth
            user.key = data['token']
            user.save()
            data['response'] = 200
            data['status'] = 'OK'
            Elogin(
                euser = user,
                datetime_text = datetime.now(),
                location = '%s'%(request.META['REMOTE_ADDR']),
                ip = request.META['REMOTE_ADDR'],
                agent = request.META['HTTP_USER_AGENT']
            ).save()
    except Exception as e:
        data['response'] = 404
        data['message'] = 'invalid Username or Password'
    return HttpResponse(json.dumps(data), content_type="application/json")
@csrf_exempt
def programmes(request,domain,auth):
    data = {'response':1,'status':'Not OK','message':''}
    try:
        key = request.POST[auth]
        token = request.GET['token']
        channel = Channel.objects.get(e_host=domain,enterprize=True)
        user = Esubscibers.objects.get(auth=auth,key=token,client=channel.who)
        #print(user)
        data['tempuser'] = user.username
        data['user'] = {}
        data['user']['name'] = '%s'%(user.name)
        data['user']['programme'] = '%s'%(user.programme.name)
        data['user']['channel'] = '%s'%(user.programme.channel.name)
        try:
            data['response'] = 200
            #print("here")
            data['status'] = 'OK'
            data['data'] = {}
            queryset = user.programme.playlist.all()
            #print(queryset)
            if(queryset.count() >= 1 ):
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
                data['data'] = res
                data['width'] = width
            else:
                data['response'] = 404
                data['status'] = 'Not OK'
                data['message'] = 'Not Data in this Programme'
                return HttpResponse(json.dumps(data), content_type="application/json")
        except Exception as e:
            data['response'] = 404
            data['status'] = 'Not OK'
            data['message'] = '%s' % (e)
            return HttpResponse(json.dumps(data), content_type="application/json")
        return HttpResponse(json.dumps(data), content_type="application/json")
    except Exception as e:
        data['response'] = 0
        data['status'] = 'Not OK'
        data['message'] = '%s' % (e)
        #print(e)
        return HttpResponse(json.dumps(data), content_type="application/json")
@csrf_exempt
def profile(request,auth,domain):
    return HttpResponse(domain)
@csrf_exempt
def messages(request,auth,domain):
    return HttpResponse(auth)