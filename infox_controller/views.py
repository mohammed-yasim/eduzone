from django.shortcuts import render,HttpResponse,Http404
import subprocess
# Create your views here.
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
@staff_member_required()
def index(request):
    return render(request,'desktop.html')
@staff_member_required()
def restart(request):
    import subprocess
    print("start")
    subprocess.call("/home/ktunss/ktunss/restart.sh")
    print("end")
    return HttpResponse("Updated PythonAnywhere successfully")
@staff_member_required()
def collectstatic(request):
    import subprocess
    print("start")
    subprocess.call("/home/ktunss/ktunss/static.sh")
    print("end")
    return HttpResponse("Updated PythonAnywhere successfully")
@staff_member_required()
def pull(request):
    import subprocess
    print("start")
    subprocess.call("/home/ktunss/ktunss/pull.sh")
    print("end")
    return HttpResponse("Updated PythonAnywhere successfully")



