from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required


@login_required(login_url='/official_admin/login')
def index(request):
    datas = {}
    return render(request,'official_admin/_status-index.html',{'datas':datas })