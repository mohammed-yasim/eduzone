from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from uuid import uuid4
import os
from dashboard_admin.models import Article
def path_and_rename_videothumb(instance, filename):
    print(instance,filename)
    upload_to = "video_thumb"
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(uuid4().hex, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)
def path_and_rename_pgm_thumb(instance, filename):
    print(instance,filename)
    upload_to = "program_thumb"
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(uuid4().hex, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)
def path_and_rename_channel_thumb(instance, filename):
    print(instance,filename)
    upload_to = "channel_thumb"
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(uuid4().hex, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class EduzonePlan(models.Model):
    custom = models.BooleanField(_("Custom Plan"),default=False)
    uid = models.CharField(_("ID"),default=uuid4, max_length=50)
    active = models.BooleanField(_("Plan Active"),default=True)
    name = models.CharField(_("Plan"), max_length=50)
    info = models.TextField(_("Plan info"),default=" ")
    validity = models.IntegerField(_("Validity"),default="90")
    price = models.IntegerField(_("Price :"),default=0)
    extra = models.IntegerField(_("Processing fee"),default=10)
    gst = models.IntegerField(_("GST Amount"),default=18)
    gst_type = models.IntegerField(_("GST(%)"),default=18)
    display_short = models.BooleanField(_("Temp Plan"),default=False)
    display_date = models.DateTimeField(_("Temp Plan Expiry"),blank=True,null=True)
    def __str__(self):
        return ("%s - (Rs %s/%s Days)" %(self.name,self.price+self.extra+self.gst,self.validity))

class Client(models.Model):
    enterprize = models.BooleanField(_("Enterprize User"),default=False)
    quota = models.IntegerField(_("Enterprize Quota"),default=0)
    uid = models.TextField(verbose_name="Channel",default=uuid4,editable=False)
    fname = models.CharField(verbose_name="First name", max_length=32)
    lname = models.CharField(verbose_name="Last name", max_length=32)
    add_1 = models.CharField(verbose_name="Address Line 1", max_length=50,default='0')
    add_2 = models.CharField(verbose_name="Address Line 2", max_length=50,default='0')
    email = models.EmailField(verbose_name="Email", max_length=254)
    mobile = models.CharField(verbose_name="Mobile Number",default=0,max_length=10)
    user = models.OneToOneField(User, verbose_name=_("Staff Account"), on_delete=models.CASCADE,blank=True,null=True,related_name='client')
    def __str__(self):
        return ("%s (%s)(%s) " %(self.fname+self.lname,self.mobile,self.email))

class Video(models.Model):
    deleted = models.BooleanField(_("Deleted"),default=False)
    name = models.CharField(verbose_name="Name", max_length=50)
    info = models.TextField(verbose_name="Description")
    icon = models.ImageField(verbose_name="Thumbnail",upload_to=path_and_rename_videothumb, null=True,blank=True,default="thumbnail_video.png")
    date = models.DateTimeField(verbose_name="BroadCast Time", auto_now=False, auto_now_add=False)
    uri = models.CharField(verbose_name="Youtube vid", max_length=64)
    uid = models.TextField(verbose_name="Channel",default=uuid4,editable=False)
    banned = models.BooleanField(_("Content Banned"),default=False)
    demo = models.BooleanField(_("Demo Video (Sample)"),default=False)
    client = models.ForeignKey(Client, verbose_name=_("Owner"), on_delete=models.CASCADE,null=True,blank=True,related_name='videos')
    class Meta:
        verbose_name = 'Video/Topic/Lesson'
        verbose_name_plural = 'Videos/Topics/Lesson'
        ordering = ['-date']
    def __str__(self):
        return ("%s (%s)" %(self.name,self.info))
    def save(self,*args, **kwargs):
        print(self.uid)
        try:
            temp = Article.objects.get(uid=self.uid)
            print(temp)
        except:
            print('created')
            Article(uid=self.uid).save()
        super(Video, self).save(*args, **kwargs)


# Create your models here.
class Categories(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    uri = models.CharField(_("URI"), max_length=50,unique=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'



class Channel(models.Model):
    enterprize = models.BooleanField(_("Enterprize Edition"),default=False)
    e_host = models.CharField(_("Enterprize Host"),default="app.studentsonly.in",max_length=64)
    name = models.CharField(verbose_name="Name", max_length=50)
    info = models.TextField(verbose_name="Description")
    icon = models.ImageField(verbose_name="Logo",upload_to=path_and_rename_channel_thumb, null=True,blank=True,default="thumbnail_video.png")
    uri = models.CharField(verbose_name="Uri", max_length=64,unique=True)
    pub = models.BooleanField(verbose_name="Published Public",default=True)
    active = models.BooleanField(verbose_name="Active",default=True)
    orderby = models.IntegerField(_("Order"),default=1000)
    category = models.ForeignKey(Categories, verbose_name="Category", related_name='channels', on_delete=models.CASCADE)
    who = models.ForeignKey(Client, verbose_name="Owner/Client", related_name='channels', on_delete=models.CASCADE)
    class Meta:
        verbose_name = '1. Channel & School'
        verbose_name_plural = '1. Channels & Schools'
        ordering = ['orderby']

    def __str__(self):
        return ("%s (%s)[%s]" %(self.name,self.who,self.orderby))

class Programme(models.Model):
    premium = models.BooleanField(_("Premium"),default=True)
    name = models.CharField(verbose_name="Name", max_length=50)
    info = models.TextField(verbose_name="Description")
    icon = models.ImageField(verbose_name="Thumbnail",upload_to=path_and_rename_pgm_thumb, null=True,blank=True,default="thumbnail_video.png")
    uri = models.CharField(verbose_name="Uri", max_length=64,unique=True)
    channel = models.ForeignKey(Channel, verbose_name="Channel", on_delete=models.CASCADE,related_name='programme')
    created = models.DateField(_("Created On"), auto_now=True)
    orderby = models.IntegerField(_("Order"),default=1000)
    custom_plan = models.BooleanField(_("Custom Plan"),default=False)
    custom_plans = models.ManyToManyField(EduzonePlan, verbose_name="Custom Plans",blank=True)
    uid = models.CharField(_("ID"),default=uuid4, max_length=50)
    class Meta:
        verbose_name = '2. Class/Programme'
        verbose_name_plural = '2. Classes/Programmes'
        ordering = ['orderby','-created']
    def __str__(self):
        return ("%s (%s)[%s]" %(self.channel.name,self.name,self.orderby))
class Playlist(models.Model):
    name = models.CharField(verbose_name="Name", max_length=50)
    uri = models.CharField(verbose_name="Uri", max_length=64,unique=True)
    programme = models.ForeignKey(Programme, verbose_name="Programme", on_delete=models.CASCADE,related_name='playlist')
    video = models.ManyToManyField(Video,verbose_name="Videos",related_name='playlist',blank=True)
    orderby = models.IntegerField(_("Order"),default=1000)
    class Meta:
        verbose_name = '3. Subject/Playlist'
        verbose_name_plural = '3. Subject/Playlists'
        ordering = ['orderby']
    def __str__(self):
        return ("%s (%s - %s) [%s]" %(self.programme.channel.name,self.programme.name,self.name,self.orderby))


class Esubscibers(models.Model):
    uid = models.CharField(_("UID"), default=uuid4, max_length=64)
    username = models.CharField(_("Username"), max_length=32)
    password = models.CharField(_("Password"), max_length=32)
    name = models.CharField(_("Name"), max_length=50,default="")
    key = models.CharField(_("KEY"), max_length=50,blank=True,default="?")
    auth = models.CharField(_("AUTH"), max_length=50,blank=True,default="?")
    programme = models.ForeignKey(Programme, verbose_name=_("Programme"), on_delete=models.CASCADE,related_name="esubscriber")
    client = models.ForeignKey(Client, verbose_name=_("Client"), on_delete=models.CASCADE,related_name="eusers")

    class Meta:
        verbose_name = 'Enterprise Subscriber'
        verbose_name_plural = 'Enterprise Subscribers'