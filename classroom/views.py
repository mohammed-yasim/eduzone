from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.contrib.admin.views.decorators import staff_member_required
@staff_member_required()
def index(request):
    return render(request,'index.html')
