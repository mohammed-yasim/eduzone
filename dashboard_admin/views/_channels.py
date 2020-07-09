from django.shortcuts import render,redirect
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime
@staff_member_required(login_url='/_admin/login')
def index(request):
    echannels = {}
    try:
        euser = request.user.client.enterprize
        if euser == True:
            echannels = request.user.client.channels.filter(enterprize=True,active=True)
    except:
        pass
    channels = request.user.client.channels.filter(enterprize=False,active=True)
    return render(request,'_admin/channels/channels.html',{
        'euser': euser,
        'echannels':echannels,
        'channels':channels
         })

@staff_member_required(login_url='/_admin/login')
def allprogrammes(request,qchannel):
    channel = request.user.client.channels.get(uri=qchannel,who=request.user.client)
    programmes = channel.programme.all()
    return render(request,'_admin/channels/programmes.html',{'programmes':programmes,'qchannel':qchannel})


@staff_member_required(login_url='/_admin/login')
def allplaylist(request,qchannel,qprogramme):
    channel = request.user.client.channels.get(uri=qchannel,who=request.user.client)
    programme = channel.programme.get(uri=qprogramme,channel=channel)
    playlist = programme.playlist.all()
    return render(request,'_admin/channels/playlists.html',{'playlists':playlist,'qchannel':qchannel,'qprogramme':qprogramme})


@staff_member_required(login_url='/_admin/login')
def videos(request,qchannel,qprogramme,qplaylist):
    channel = request.user.client.channels.get(uri=qchannel,who=request.user.client)
    programme = channel.programme.get(uri=qprogramme,channel=channel)
    playlist = programme.playlist.get(uri=qplaylist,programme=programme)
    videos = playlist.video.filter(deleted=False,banned=False,client=request.user.client).extra(where=['date<%s'], params=[datetime.now()]).order_by('-date')
    return render(request,'_admin/channels/videos.html',{'videos':videos,'qchannel':qchannel,'qprogramme':qprogramme})
