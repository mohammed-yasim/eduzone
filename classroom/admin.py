from django.contrib import admin
from .models import Profile,SubscriptionList,EduzoneOrder
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    readonly_fields=('user',)#'subscribed')

admin.site.register(Profile,ProfileAdmin)
admin.site.register(SubscriptionList)
admin.site.register(EduzoneOrder)
