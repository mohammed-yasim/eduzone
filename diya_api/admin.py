from django.contrib import admin
from .models import Channel,Client,Programme,Playlist,Video,Categories,EduzonePlan
# Register your models here.
admin.site.register(Channel)
admin.site.register(Client)
admin.site.register(Programme)
admin.site.register(Playlist)
admin.site.register(Video)
admin.site.register(Categories)
class EduzonePlansAdmin(admin.ModelAdmin):
    readonly_fields=('uid',)#'subscribed')
admin.site.register(EduzonePlan,EduzonePlansAdmin)
