from django.shortcuts import render,HttpResponse
import json
# Create your views here.
def index(request):
    data = """{
    "short_name": "StudentsOnly",
    "name": "StudentsOnly.in The learning App",
    "start_url": ".",
    "icons": [{
        "src": "/app/favicon.ico",
        "sizes": "48x48",
        "type": "image/x-icon"
    }, {
        "src": "/app/android-chrome-192x192.png",
        "sizes": "192x192",
        "type": "image/png"
    }, {
        "src": "/app/android-chrome-512x512.png",
        "sizes": "512x512",
        "type": "image/png"
    }],
    "theme_color": "#BF3A3A",
    "background_color": "#e0e0e0",
    "display": "standalone"
  }
    """
    datas = json.loads(data)
    return HttpResponse(json.dumps(datas), content_type="application/json")
def service(request):
    return render(request,'service-worker.js',content_type=" text/javascript")
def service2(request,query='0'):
    return render(request,'precache-manifest.%s.js'%(query),content_type=" text/javascript")
    
