from django.contrib.auth.forms import (
    UserCreationForm,
)
from django.contrib.auth.models import (
    User,
)
from django.forms import ModelForm


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
