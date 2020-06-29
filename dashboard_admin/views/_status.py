from django.shortcuts import render,redirect
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required(login_url='/_admin/login')
def index(request):
    datas = {}
    return render(request,'_admin/_status-index.html',{'datas':datas })