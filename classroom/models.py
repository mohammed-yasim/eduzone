from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from diya_api.models import Programme


from django.utils.translation import gettext_lazy as _
class SubscriberpaymentList(models.Model):
    date = models.DateField(_("Date"), auto_now=False, auto_now_add=False)
    payment_id=models.CharField(_("Payment ID"), max_length=50,blank=True)
    subscribed = models.OneToOneField(Programme, verbose_name=_("Channel"), on_delete=models.CASCADE)
    def __str__(self):
        return self.subscribed.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #mobile = models.CharField(_("Mobile No"), max_length=10,default="0")
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    subscribed = models.ManyToManyField(SubscriberpaymentList,related_name='subscribers')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()