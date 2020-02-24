from django.urls import (
    path,
)
from django.contrib.auth import views as auth_views
from users.views import (
    # MyLoginView,
    RegisterView,
    # LogoutView,
    SettingsView,
)
from users.forms import (
    LoginForm,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    # path('login/', LoginView.as_view(), name='login'),
    path('login/',
         auth_views.LoginView.as_view(
             template_name='login.html',
             authentication_form=LoginForm,
             redirect_authenticated_user=False,),
         name='login'
         ),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path('logout/',
         auth_views.LogoutView.as_view(
             template_name='logout.html',
         ),
         name='logout'),
    path('edit/', SettingsView.as_view(), name='settings'),
]
