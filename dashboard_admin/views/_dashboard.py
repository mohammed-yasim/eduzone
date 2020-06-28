from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required(login_url='/_admin/login')
def index(request):
    datas = {}
    return render(request,'_admin/_dashboard-index.html',{'datas':datas })