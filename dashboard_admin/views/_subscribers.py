from django.shortcuts import render,redirect,HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from diya_api.models import Esubscibers,Programme
import json
from django.core import serializers



@staff_member_required(login_url='/_admin/login')
def index(request):
    datas = {}
    datas['channels'] = request.user.client.channels.filter(active=True)
    return render(request,'_admin/users/all.html',{'datas':datas })

@staff_member_required(login_url='/_admin/login')
def addser(request):
    try:
        pgm = request.POST['pgm']
        programme = Programme.objects.get(uid=pgm)
        Esubscibers(
            username = request.POST['username'],
            password = request.POST['password'],
            name =request.POST['name'], 
            details = request.POST['details'],
            contact = request.POST['contact'],
            programme = programme,
            client = request.user.client
        ).save()
        return redirect('/_admin/subscribers')
    except Exception as e:
        return  redirect('/_admin')
@staff_member_required(login_url='/_admin/login')
def never_logged(request):
    data = request.user.client.eusers.filter(auth="?",key="?")
    data = serializers.serialize('json', data)
    var_list = []
    for data in json.loads(data):
        var_list.append(data['fields']['name'])
    data= var_list
    return HttpResponse(json.dumps(data), content_type="application/json")
@staff_member_required(login_url='/_admin/login')
def logged(request):
    data = request.user.client.eusers.exclude(auth="?",key="?")
    data = serializers.serialize('json', data)
    var_list = []
    for data in json.loads(data):
        var_list.append(data['fields']['name'])
    data= var_list
    return HttpResponse(json.dumps(data), content_type="application/json")
