from django.contrib import admin
from .models import Profile,SubscriberpaymentList
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields=('user',)#'subscribed')
admin.site.register(Profile,ProfileAdmin)
admin.site.register(SubscriberpaymentList)