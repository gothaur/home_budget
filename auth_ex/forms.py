from django.conf import settings
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
from captcha.fields import (
    ReCaptchaField,
)
from captcha.widgets import (
    ReCaptchaV2Checkbox,
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
    send_email = forms.BooleanField(
        required=False,
        # label='Chcę otrzymywać miesięczy raport wydatków',
    )

    text = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'aria-label': 'Text input with checkbox',
                'placeholder': 'Wysyłaj mi miesięczy raport wydatków',
            }
        ),
        required=False,
        disabled=True,
        label='',
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
    # captcha = ReCaptchaField(
    #     public_key=settings.GOOGLE_RECAPTCHA_SITE_KEY,
    #     private_key=settings.GOOGLE_RECAPTCHA_SECRET_KEY,
    #     widget=ReCaptchaV2Checkbox(
    #         api_params={
    #             'hl': 'pl',
    #         }
    #     ),
    # )

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2']

    # def clean_captcha(self):
    #     captcha = self.cleaned_data.get("captcha")
    #     print(captcha)
    #     if not captcha['success']:
    #         raise forms.ValidationError(
    #             self.error_messages['Czy aby na pewno jesteś człowkiem?'],
    #         )
    #     return captcha


class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validate_file_extension])
