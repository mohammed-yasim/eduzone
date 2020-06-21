from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django import forms

class UserLoginForm(AuthenticationForm):

    error_messages = {
        **AuthenticationForm.error_messages,
        'invalid_login': _(
            "Please enter the correct %(username)s and password."
            " Note that both fields may be case-sensitive."
        ),
    }
    required_css_class = 'required'
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'autofocus':'',
            'placeholder': 'Enter your Username...', 'id': 'hello',
        'data-validate':"required minlength=5",
        'data-role':"input",
        'data-prepend':"<span class='mif-envelop'>"
        }))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter your Password...',
            'id': 'hi',
            'data-validate':"required minlength=6",
        'data-role':"input",
        'data-prepend':"<span class='mif-key'>"
        }
))

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    required_css_class = 'required'
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
    username = forms.CharField(max_length=30,widget=forms.TextInput(
        attrs={'autofocus':'',
            'placeholder': 'Enter your Username...', 'id': 'hello',
        'data-validate':"required minlength=5",
        'data-role':"input",
        'data-prepend':"<span class='mif-envelop'>"
        }))
    mobile = forms.CharField(max_length=10,widget=forms.TextInput(
        attrs={'autofocus':'',
        'type':'tel',
            'placeholder': 'Enter your Mobile...', 'id': 'hello',
        'data-validate':"required minlength=5",
        'data-role':"input",
        'data-prepend':"<span class='mif-envelop'>",
        }))

    class Meta:
        model = User
        fields = ('first_name','last_name','username', 'password1', 'password2','mobile')