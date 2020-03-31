from django.contrib.auth import (
    get_user_model,
)
from django.urls import (
    path,
    reverse_lazy)
from django.contrib.auth import views as auth_views
from django.views.generic import (
    DeleteView,
)
from auth_ex.views import (
    RegisterView,
    SettingsView,
    SignInCategory,
    SignOutCategory,
    StatuteView,
)
from auth_ex.forms import (
    LoginForm,
)

app_name = 'auth_ex'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/',
         auth_views.LoginView.as_view(
             template_name='auth_ex/login.html',
             authentication_form=LoginForm,
             redirect_authenticated_user=False, ),
         name='login'
         ),
    path('logout/',
         auth_views.LogoutView.as_view(
             template_name='auth_ex/logout.html',
         ),
         name='logout'),
    path('edit/', SettingsView.as_view(), name='settings'),
    path(
        'reset-password/',
        auth_views.PasswordResetView.as_view(
            email_template_name='auth_ex/password-reset-email.html',
            template_name='auth_ex/password-reset-form.html',
            success_url=reverse_lazy('auth_ex:password-reset-done'),
        ),
        name='password-reset'
    ),
    path(
        'reset-password/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='auth_ex/password-reset-done.html',
        ),
        name='password-reset-done'
    ),
    path(
        'reset-password/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
            template_name='auth_ex/password-reset-confirm.html',
            success_url=reverse_lazy('auth_ex:password-reset-complete')
        ),
        name='password-reset-confirm',
    ),
    path(
        'reset-password/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='auth_ex/password-reset-complete.html'
        ),
        name='password-reset-complete',
    ),
    path('category/delete/<int:category_id>/', SignOutCategory.as_view(), name='signout-category'),
    path('category/add/<int:category_id>/', SignInCategory.as_view(), name='signin-category'),
    path('statute/', StatuteView.as_view(), name='statute'),
    path(
        'delete/<int:user_id>',
        DeleteView.as_view(
            template_name='auth_ex/delete.html',
            model=get_user_model(),
            pk_url_kwarg='user_id',
            success_url=reverse_lazy(
                'auth_ex:register',
            ),
        ),
        name='delete-user',
    ),
]
