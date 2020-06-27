from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from diya_api.models import Programme,EduzonePlan
from django.utils.translation import gettext_lazy as _
from uuid import uuid4


class EduzoneOrder(models.Model):
    date = models.DateTimeField(_("Order Created"), auto_now=True)
    order = models.CharField(_("Order ID"),default=0, max_length=128)
    plan = models.ForeignKey(EduzonePlan, verbose_name=_("Plan"), on_delete=models.CASCADE,related_name='order')
    programme = models.ForeignKey(Programme, verbose_name=_("Channel"), on_delete=models.CASCADE,related_name='order')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='order')
    status = models.BooleanField(_("Success"),default=False)
    razor_id = models.CharField(_("Razorpay Order ID"),default=" ",max_length=128)
    razor_status = models.CharField(_("Razorpay Status"),default=" ",max_length=64)
    razor_amount = models.IntegerField(_("Razorpay Amount"),default=0)
    razor_created = models.CharField(_("Razorpay created"),default=" ",max_length=50)
    paid = models.BooleanField(_("Amount Paid"),default=False)
    cancelled = models.BooleanField(_("Order Cancelled"),default=False)
    def __str__(self):
        return ("%s | %s_%s %s - %s:%s")%(self.razor_status,self.programme.channel.name,self.programme.name,self.plan,self.user.username,self.date)

class EduzonePay(models.Model):
    date = models.DateTimeField(_("Order Created"), auto_now=True)
    pay = models.CharField(_("Payment ID"), max_length=50)
    razor_id = models.CharField(_("Razorpay Order ID"),default=" ",max_length=128)
    razor_pay=models.CharField(_("Razorpay Payment ID"), max_length=128,blank=True)
    razor_email = models.TextField(_("Rozor Email"),default="")
    razor_mobile = models.TextField(_("Razor Mobile"),default="")
    razor_amount = models.IntegerField(_("Razorpay Amount"),default=0)
    razor_sign = models.TextField(_("Razor Sign"),default="")
    razorpay_text = models.TextField(_("Rozorpay Text"),default="")


class SubscriptionList(models.Model):
    date = models.DateTimeField(_("Date"), auto_now=True,)
    eduzone_order = models.CharField(_("Order ID"), max_length=128,blank=True)
    razor_pay = models.CharField(_("Razorpay payment ID"),default=" ",max_length=128)
    plan = models.ForeignKey(EduzonePlan, verbose_name=_("Plan"),on_delete=models.CASCADE,related_name='subscribers')
    programme = models.ForeignKey(Programme, verbose_name=_("Channel"),on_delete=models.CASCADE,related_name='subscriber',)
    is_activated = models.BooleanField(_("Active"),default=True)
    expiry = models.TextField(_("Plan Expiry"),default="0")
    validity = models.IntegerField(_("Validity"),default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    def __str__(self):
        return self.programme.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    mobile = models.CharField(_("Mobile No"), max_length=10,default="0")
    school = models.TextField(_("School : "),default=" ")
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



