from django.db import models
from diya_api.models import Programme,Client
from django.utils.translation import gettext_lazy as _
from uuid import uuid4

# Create your models here.
class Esubscibers(models.Model):
    uid = models.CharField(_("UID"), default=uuid4, max_length=64)
    username = models.CharField(_("Username"), max_length=32)
    password = models.CharField(_("Password"), max_length=32)
    name = models.CharField(_("Name"), max_length=50,default="")
    programme = models.ForeignKey(Programme, verbose_name=_("Programme"), on_delete=models.CASCADE,related_name="esubscriber")
    client = models.ForeignKey(Client, verbose_name=_("Client"), on_delete=models.CASCADE,related_name="eusers")
    def __str__(self):
        pass

    class Meta:
        verbose_name = 'Enterprise Subscriber'
        verbose_name_plural = 'Enterprise Subscribers'





class Replies(models.Model):
    uid = models.CharField(_("Unique ID"), default=uuid4,max_length=64)
    text = models.TextField(_("Reply"),default="")
    user = models.CharField(_("username"), max_length=50)
    class Meta:
        verbose_name = _("Reply")
        verbose_name_plural = _("Replies")
        
class Comment(models.Model):
    uid = models.CharField(_("Unique ID"), default=uuid4,max_length=64)
    text = models.TextField(_("Reply"),default="")
    user = models.CharField(_("username"), max_length=50)
    reply = models.ManyToManyField(Replies, verbose_name=_("Replies"),blank=True,related_name="comment")
    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

class Article(models.Model):
    uid = models.CharField(_("Unique ID"), default='0',max_length=64)
    likes = models.IntegerField(_("Likes"),default=0)
    dislikes = models.IntegerField(_("Dislikes"),default=0)
    comment = models.ManyToManyField(Comment, verbose_name=_("Comments"),blank=True,related_name='article')
    text = models.TextField(_("Content"),blank=True,default="")
    def __str__(self):
        return self.uid
    
    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
    

