from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
import razorpay,json
from uuid import uuid4

def app(request,path=0):
    return render(request,'static/index.html')

from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def home_view(request):
    #return render(request, 'home.html')
    return HttpResponse(request.user.profile)

from .forms import SignUpForm
from .models import Profile

def signup_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.profile.first_name = form.cleaned_data.get('first_name')
        user.profile.last_name = form.cleaned_data.get('last_name')
        user.profile.mobile = form.cleaned_data.get('mobile')
        user.profile.school = form.cleaned_data.get('school')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
def pview(request):
    payudat = {
        'amount':100,
        'currency':'INR',
        'receipt':'%s' %(uuid4()),
        'payment_capture' : 1,
    }
    client = razorpay.Client(auth=("rzp_test_3wsCGY19wKp607", "L7LUV805Iwae4Qtnfy6znjls"))
    #try:
    odersdata = json.dumps(payudat)
    aa = client.order.create(data=payudat)
    bb = client.payment.capture(payudat['receipt'], payudat['amount'], {"currency": payudat['currency']})
    return HttpResponse(json.dumps(bb))