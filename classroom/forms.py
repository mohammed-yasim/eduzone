from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
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
        attrs={'autofocus': '',
               'placeholder': 'Enter Username...', 'id': 'hello',
               'data-validate': "required minlength=5",
               'data-role': "input",
               'data-prepend': "<span class='mif-envelop'>"
               }))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter Password...',
            'id': 'hi',
            'data-validate': "required minlength=6",
            'data-role': "input",
            'data-prepend': "<span class='mif-key'>"
        }
    ))


class SignUpForm(UserCreationForm):
    error_messages = {
        **UserCreationForm.error_messages,
        'invalid_login': _(
            "Please enter the correct %(username)s and password."
            " Note that both fields may be case-sensitive."
        ),
    }
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={
            'autofocus': '',
            'type': 'text',
            'id': 'defaultRegisterFormFirstName',
            'class': "form-control",
            'placeholder': "First name",
            'required': '',
            'pattern':".{4,}",
        }))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={
            'type': 'text',
            'id': 'defaultRegisterFormLastName',
            'class': "form-control",
            'placeholder': "Last name",
            'required': ''
        }))
    school = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={
            'type': 'text',
            'id': 'defaultRegisterFormLastName',
            'class': "form-control mb-4",
            'placeholder': "School/institution Address",
            'required': '',
            'pattern':".{10,}",
        }))
    username = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={
            'type': "username",
            'id': "validationCustomUsername",
            'class': "form-control",
            'placeholder': "Username",
            'required': '',
            'pattern':".{6,}",
            'title':'username must be 6 letters'
        }))
    password1 = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={
            'type': "password",
            'id': "defaultRegisterFormUsername",
            'class': "form-control mb-4",
            'placeholder': "Password",
            'pattern':".{6,}",
            'required': ''
        }))
    password2 = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={
            'type': "password",
            'id': "defaultRegisterFormUsername",
            'class': "form-control mb-4",
            'placeholder': "Confirm Password",
            'pattern':".{6,}",
            'required': ''
        }))
    mobile = forms.CharField(max_length=10, widget=forms.TextInput(
        attrs={
            'type': "tel",
            'id': "defaultRegisterFormUsername",
            'class': "form-control mb-4",
            'placeholder': "Mobile Number",
            'required': '',
            'size':10,
            'maxlength':10,
            'oninput':"this.value = this.value.replace(/[^0-9.]/g, '').replace(/(\..*)\./g, '$1');",
            'pattern':"[0-9]{10}"
        }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'school',
                  'username', 'password1', 'password2', 'mobile')
