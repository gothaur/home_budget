from django.contrib.auth.forms import (
    AuthenticationForm,
)
from django import forms
from budget.models import (
    Category,
)


class EditUserForm(forms.Form):
    form_name = forms.CharField(
        widget=forms.HiddenInput(
            attrs={
                'value': 'edit_user',
            }
        ),
    )
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-3',
            }
        ),
        label='Login',
        disabled=True,
        required=False
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Imię',
            }),
        label='',
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Nazwisko',
            }),
        label='',
    )
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'email',
            }),
        label='',
        required=False,
    )


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


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
