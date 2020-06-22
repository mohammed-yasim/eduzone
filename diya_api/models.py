from django.db import models
from django.utils.translation import gettext_lazy as _
from uuid import uuid4
import os
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
    name = models.CharField(_("Plan"), max_length=50)
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
    uid = models.TextField(verbose_name="Channel",default=uuid4,editable=False)
    fname = models.CharField(verbose_name="First name", max_length=32)
    lname = models.CharField(verbose_name="Last name", max_length=32)
    add_1 = models.CharField(verbose_name="Address Line 1", max_length=50,default='0')
    add_2 = models.CharField(verbose_name="Address Line 2", max_length=50,default='0')
    email = models.EmailField(verbose_name="Email", max_length=254)
    mobile = models.IntegerField(verbose_name="Mobile Number",default=0)
    def __str__(self):
        return ("%s (%s)" %(self.fname+self.lname,self.mobile))

class Video(models.Model):
    name = models.CharField(verbose_name="Name", max_length=50)
    info = models.TextField(verbose_name="Description")
    icon = models.ImageField(verbose_name="Thumbnail",upload_to=path_and_rename_videothumb, null=True,blank=True,default="thumbnail_video.png")
    date = models.DateTimeField(verbose_name="BroadCast Time", auto_now=False, auto_now_add=False)
    uri = models.CharField(verbose_name="Youtube vid", max_length=64)
    uid = models.TextField(verbose_name="Channel",default=uuid4,editable=False)
    banned = models.BooleanField(_("Content Banned"),default=False)
    demo = models.BooleanField(_("Demo Video (Sample)"),default=False)
    class Meta:
        verbose_name = '4. Video/Topic/Lesson'
        verbose_name_plural = '4. Videos/Topics/Lesson'
        ordering = ['-date']
    def __str__(self):
        return ("%s (%s)" %(self.name,self.info))

# Create your models here.
class Categories(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    uri = models.CharField(_("URI"), max_length=50)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'



class Channel(models.Model):
    name = models.CharField(verbose_name="Name", max_length=50)
    info = models.TextField(verbose_name="Description")
    icon = models.ImageField(verbose_name="Logo",upload_to=path_and_rename_channel_thumb, null=True,blank=True,default="thumbnail_video.png")
    uri = models.CharField(verbose_name="Uri", max_length=64)
    pub = models.BooleanField(verbose_name="Published",default=True)
    active = models.BooleanField(verbose_name="Active",default=True)
    orderby = models.IntegerField(_("Order"),default=1000)
    category = models.ForeignKey(Categories, verbose_name="Category", related_name='channels', on_delete=models.CASCADE)
    who = models.ForeignKey(Client, verbose_name="Owner", related_name='channels', on_delete=models.CASCADE)
    class Meta:
        verbose_name = '1. Channel & School'
        verbose_name_plural = '1. Channels & Schools'
        ordering = ['orderby']

    def __str__(self):
        return ("%s (%s)[%s]" %(self.name,self.who,self.orderby))
class Programme(models.Model):
    premium = models.BooleanField(_("Premium"),default=False)
    name = models.CharField(verbose_name="Name", max_length=50)
    info = models.TextField(verbose_name="Description")
    icon = models.ImageField(verbose_name="Thumbnail",upload_to=path_and_rename_pgm_thumb, null=True,blank=True,default="thumbnail_video.png")
    uri = models.CharField(verbose_name="Uri", max_length=64)
    channel = models.ForeignKey(Channel, verbose_name="Channel", on_delete=models.CASCADE)
    created = models.DateField(_("Created On"), auto_now=True)
    orderby = models.IntegerField(_("Order"),default=1000)
    custom_plan = models.BooleanField(_("Custom Plan"),default=False)
    custom_plans = models.ManyToManyField(EduzonePlan, verbose_name="Custom Plans")
    
    class Meta:
        verbose_name = '2. Class/Programme'
        verbose_name_plural = '2. Classes/Programmes'
        ordering = ['orderby','-created']
    def __str__(self):
        return ("%s (%s)[%s]" %(self.channel.name,self.name,self.orderby))
class Playlist(models.Model):
    name = models.CharField(verbose_name="Name", max_length=50)
    uri = models.CharField(verbose_name="Uri", max_length=64)
    programme = models.ForeignKey(Programme, verbose_name="Programme", on_delete=models.CASCADE)
    video = models.ManyToManyField(Video, verbose_name="Videos")
    orderby = models.IntegerField(_("Order"),default=1000)
    class Meta:
        verbose_name = '3. Subject/Playlist'
        verbose_name_plural = '3. Subject/Playlists'
        ordering = ['orderby']
    def __str__(self):
        return ("%s (%s - %s) [%s]" %(self.programme.channel.name,self.programme.name,self.name,self.orderby))



