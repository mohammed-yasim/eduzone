from django.shortcuts import render,redirect,HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from diya_api.models import Esubscibers,Programme

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
