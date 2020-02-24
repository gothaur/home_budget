from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
)
from django.contrib.auth.models import (
    User,
)
from django import forms


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Nazwa użytkownika',
            }),
        label='',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Hasło',
            }),
        label='',
    )
