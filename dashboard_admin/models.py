from django.db import models
from django.utils.translation import gettext_lazy as _
from uuid import uuid4

# Create your models here.

class Replies(models.Model):
    uid = models.CharField(_("Unique ID"), default=uuid4,max_length=64)
    text = models.TextField(_("Reply"),default="")
    user = models.CharField(_("username"), max_length=50)
    date = models.DateTimeField(_("Date time"), auto_now=True)
    class Meta:
        verbose_name = _("Reply")
        verbose_name_plural = _("Replies")
        
class Comment(models.Model):
    uid = models.CharField(_("Unique ID"), default=uuid4,max_length=64)
    text = models.TextField(_("Reply"),default="")
    user = models.CharField(_("username"), max_length=50,default='')
    name = models.CharField(_("Name"), max_length=32,default='')
    date = models.DateTimeField(_("Date time"), auto_now=True)
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
    

