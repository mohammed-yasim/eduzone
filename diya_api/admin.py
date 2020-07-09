from django.contrib import admin
from .models import Channel,Client,Programme,Playlist,Video,Categories,EduzonePlan,Esubscibers,Ewatch,Elogin
# Register your models here.
admin.site.register(Channel)
admin.site.register(Client)
admin.site.register(Programme)
admin.site.register(Playlist)
admin.site.register(Video)
admin.site.register(Categories)
admin.site.register(Esubscibers)
class EloginAdmin(admin.ModelAdmin):
    readonly_fields=('euser',)
admin.site.register(Elogin,EloginAdmin)
class EwatchAdmin(admin.ModelAdmin):
    readonly_fields=('euser','video','url')
admin.site.register(Ewatch,EwatchAdmin)
class EduzonePlansAdmin(admin.ModelAdmin):
    readonly_fields=('uid',)
admin.site.register(EduzonePlan,EduzonePlansAdmin)
