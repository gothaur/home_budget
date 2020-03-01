from django.urls import (
    path,
)
from django.contrib.auth import views as auth_views
from users.views import (
    RegisterView,
    SettingsView,
    SignInCategory,
    SignOutCategory,
    StatuteView,
)
from users.forms import (
    LoginForm,
)

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/',
         auth_views.LoginView.as_view(
             template_name='users/login.html',
             authentication_form=LoginForm,
             redirect_authenticated_user=False,),
         name='login'
         ),
    path('logout/',
         auth_views.LogoutView.as_view(
             template_name='users/logout.html',
         ),
         name='logout'),
    path('edit/', SettingsView.as_view(), name='settings'),
    path('category/delete/<int:category_id>/', SignOutCategory.as_view(), name='signout-category'),
    path('category/add/<int:category_id>/', SignInCategory.as_view(), name='signin-category'),
    path('statute/', StatuteView.as_view(), name='statute'),
]
