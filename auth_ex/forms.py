from django.contrib.auth import (
    get_user_model,
)
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
)
from django import forms
from budget.models import (
    Category,
)
from home_budget.validators import (
    validate_file_extension,
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


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2']


class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validate_file_extension])
