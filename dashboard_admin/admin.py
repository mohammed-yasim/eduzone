from django.contrib import admin
from .models import Esubscibers,Article,Comment,Replies
# Register your models here.
admin.site.register(Esubscibers)
admin.site.register(Replies)
admin.site.register(Comment)
admin.site.register(Article)
