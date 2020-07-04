from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from diya_api.models import Programme,EduzonePlan
from datetime import datetime
from uuid import uuid4
import razorpay,json
# Create your views here.
from django.contrib.auth.decorators import login_required
@login_required(login_url="/_accounts/login")
def index(request):
    s=datetime.now().timestamp() * 1000
    temp = uuid4()
    data = {}
    data['token'] = temp
    key = request.GET['p']
    pgm = Programme.objects.get(uid=key)
    data['program'] = pgm
    if pgm.custom_plan == False  and pgm.channel.enterprize == False:
        today = datetime.now()
        plans = EduzonePlan.objects.filter(custom=False,display_short=False,active=True)
        temp_plans = EduzonePlan.objects.filter(custom=False,display_short=True,active=True).extra(where=['display_date>%s'],params=[today])
        data['plans'] = plans
        data['temp_plans'] = temp_plans
        u = datetime.now().timestamp() * 1000
        print(u-s)
        return render(request,'plans.html',{'data':data})
    else:
          return HttpResponse("""
          <meta name="viewport" content="width=device-width,initial-scale=1">
        <h3>You don't have access to subscribe this channel</h3>
        <p>For more information contact helpline</p>

        <script>
        setTimeout(function(){
        window.close()
        },3000);
        </script>""")