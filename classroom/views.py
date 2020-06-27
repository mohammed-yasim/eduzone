from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
import razorpay,json
from uuid import uuid4
from datetime import datetime,timedelta
def app(request,path=0):
    return render(request,'static/index.html')

from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def home_view(request):
    #return render(request, 'home.html')
    return HttpResponse(request.user.order.all())

from .forms import SignUpForm
from .models import Profile,EduzoneOrder,EduzonePay,SubscriptionList
from diya_api.models import Programme as Programme2,EduzonePlan as EduzonePlan2

def signup_view(request):
    print(request)
    if request.POST:
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.mobile = form.cleaned_data.get('mobile')
            user.profile.school = form.cleaned_data.get('school')
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
        return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})



@login_required(login_url="_accounts/login")
def makeOrder(request):
    key = 'rzp_test_3wsCGY19wKp607'
    secret = 'L7LUV805Iwae4Qtnfy6znjls'

    status = False
    data = {}
    data['key'] = key
    if request.POST and request.session.get('C_ORDER') !=  request.POST['csrfmiddlewaretoken']:
        try:
            pgm_q = request.POST['p']
            plan_q = request.POST['plan']
            programme = Programme2.objects.get(uid=pgm_q)
            plan = EduzonePlan2.objects.get(uid=plan_q)
            payudat = {
                'amount':int(plan.price+plan.extra+plan.gst)*100,
                'currency':'INR',
                'receipt':'%s' %(uuid4()),
                'payment_capture' : 0,
                'notes' : ['Package : %s %s - %s'%(programme.name,programme.channel.name,plan)]
            }
            client = razorpay.Client(auth=(data['key'], secret))
            order_razorpay = client.order.create(data=payudat)
            neworder = EduzoneOrder(
                order = order_razorpay['receipt'],
                plan = plan,
                programme = programme,
                user = request.user,
                razor_id = order_razorpay['id'],
                razor_status = order_razorpay['status'],
                razor_amount = order_razorpay['amount'],
                razor_created = order_razorpay['created_at']
                )
            status = True
        except Exception as e :
            return HttpResponse(e)
        finally:
            if status==True:
                neworder.save()
                data['order'] = neworder
                data['info'] = payudat['notes'][0]
                request.session['C_ORDER'] = request.POST['csrfmiddlewaretoken']
        return render(request,'razorpay.html',{'data':data})

    else:
        returndata = """
         <html>
         <head>
         <title>Payment</title>
         </head>
         <body>
         <h1>Invalid Token</h1>
         <script>
         setTimeout(function(){ alert('Error : Invalid Tokenm'); window.close() }, 100);
         </script>
         </body>
         </html>
        """
        return HttpResponse(returndata)
def payment_check(request):
    key = 'rzp_test_3wsCGY19wKp607'
    secret = 'L7LUV805Iwae4Qtnfy6znjls'
    if request.method=='POST':
        client = razorpay.Client(auth=(key, secret))
        razorpay_payment_id = request.POST['razorpay_payment_id']
        razorpay_order_id = request.POST['razorpay_order_id']
        razorpay_signature = request.POST['razorpay_signature']
        order = EduzoneOrder.objects.get(razor_id = razorpay_order_id)
        payment = client.payment.capture(razorpay_payment_id, order.razor_amount, { 'currency':'INR',})
        epayment = EduzonePay(
            pay = order.order,
            razor_id = payment['order_id'],
            razor_pay = payment['id'],
            razor_email = payment['email'],
            razor_mobile = payment['contact'],
            razor_amount = payment['amount'],
            razor_sign = razorpay_signature,
            razorpay_text = json.dumps(payment))
        epayment.save()
        subscribe = SubscriptionList(
            eduzone_order = order.order,
            razor_pay = payment['id'],
            plan = order.plan,
            programme = order.programme,
            is_activated = True,
            expiry = datetime.now() - timedelta(days=int(order.plan.validity)),
            validity = order.plan.validity,
            user = request.user
        )
        subscribe.save()
        order.paid = True
        order.razor_status = "Paid " +payment['status']
        order.save()
    else:
        return HttpResponse("<script>window.close();window.location = 'https://studentsonly.in' </script>")
    return HttpResponse("<script>window.close();</script>")