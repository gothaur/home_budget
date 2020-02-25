from django.urls import (
    path,
)
from django.contrib.auth import views as auth_views
from users.views import (
    RegisterView,
    SettingsView,
)
from users.forms import (
    LoginForm,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/',
         auth_views.LoginView.as_view(
             template_name='login.html',
             authentication_form=LoginForm,
             redirect_authenticated_user=False,),
         name='login'
         ),
    path('logout/',
         auth_views.LogoutView.as_view(
             template_name='logout.html',
         ),
         name='logout'),
    path('edit/', SettingsView.as_view(), name='settings'),
]
