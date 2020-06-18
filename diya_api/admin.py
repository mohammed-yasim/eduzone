from django.contrib import admin
from .models import Channel,Client,Programme,Playlist,Video
# Register your models here.
admin.site.register(Channel)
admin.site.register(Client)
admin.site.register(Programme)
admin.site.register(Playlist)
admin.site.register(Video)
