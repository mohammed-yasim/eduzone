from django.contrib import admin
from .forms import UserLoginForm
from django.views.generic import TemplateView
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group,User
from django.utils.translation import ugettext, ugettext_lazy as _
class Infox_Security(UserAdmin):
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        if request.user.is_superuser:
            perm_fields = ('is_active', 'is_staff', 'is_superuser',
                           'groups', 'user_permissions')
        else:
            # modify these to suit the fields you want your
            # staff user to be able to edit
            perm_fields = ('is_active', 'is_staff')

        return [(None, {'fields': ('username', 'password')}),
                (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
                (_('Permissions'), {'fields': perm_fields}),
                (_('Important dates'), {'fields': ('last_login', 'date_joined')})]

admin.site.site_header = "InfoX Securtity"
admin.site.site_title = "Infox Security"
admin.site.index_title = "Welcome to Infox Security Dashboard"
admin.site.login_form = UserLoginForm
admin.site.login_template = "system_index.html"
#admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User, Infox_Security)

# Register your models here.

