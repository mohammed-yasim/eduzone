from django.shortcuts import render,redirect
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime
from dashboard_admin.models import Article

@staff_member_required(login_url='/_admin/login')
def index(request):
    videos = request.user.client.videos.filter(deleted=False,banned=False).extra(where=['date<%s'], params=[datetime.now()]).order_by('-date')
    return render(request,'_admin/_videos-index.html',{'videos':videos })

@staff_member_required(login_url='/_admin/login')
def editvideo(request,vid):
    data = {}
    if request.POST:
        try:
            videoeditname = request.POST['videoeditname']
            videoeditinfo = request.POST['videoeditinfo']
            videoeditarticle = request.POST['videoeditarticle']
            videoedit = request.user.client.videos.get(uid=vid)
            videoedit.name = videoeditname
            videoedit.info = videoeditinfo
            videoedit.save()
            articleedit = Article.objects.get(uid=vid)
            articleedit.text = videoeditarticle
            articleedit.save()
            data['edit'] = 'success'
            data['edit_message'] = 'Saved Successfully'
        except Exception as e:
            data['edit'] = 'error'
            data['edit_message'] = e
    video = request.user.client.videos.get(uid=vid)
    article = Article.objects.get(uid=vid)
    return render(request,'_admin/_videos-edit.html',{'data':data,'video':video,'article':article })
