from django.shortcuts import render,redirect
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime

@staff_member_required(login_url='/_admin/login')
def index(request):
    videos = request.user.client.videos.filter(deleted=False,banned=False).extra(where=['date<%s'], params=[datetime.now()]).order_by('-date')
    return render(request,'_admin/_videos-index.html',{'videos':videos })