from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django import forms

class UserLoginForm(AuthenticationForm):

    error_messages = {
        **AuthenticationForm.error_messages,
        'invalid_login': _(
            "Please enter the correct %(username)s and password for a staff "
            "account. Note that both fields may be case-sensitive."
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
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )