from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import (
    User,
)
from django.shortcuts import (
    render,
    redirect,
)
from django.views import (
    View,
)
from budget.models import (
    Category,
)


class LoginView(View):

    def get(self, request):
        logout(request)
        return render(request, 'login.html')

    def post(self, request):

        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            # if user.is_active():
            login(request, user)
            request.session['username'] = user.username
            return redirect(request.GET.get('next', '/'))

        return redirect('login')


class RegisterView(View):

    def get(self, request):
        form = UserCreationForm()
        context = {
            'form': form,
        }
        return render(request, 'register.html', context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            context = {
                'form': form,
            }
            return render(request, 'register.html', context)


# class RegisterView(View):
#
#     def get(self, request):
#         return render(request, 'register.html')
#
#     def post(self, request):
#         username = request.POST.get('username')
#         pass1 = request.POST.get('password_1')
#         pass2 = request.POST.get('password_2')
#
#         if username is not None and len(username) > 6:
#             if pass1 == pass2 and pass1 is not None and len(pass1) > 6:
#                 User.objects.create_user(username=username, password=pass1)
#                 return redirect('login')
#
#         return render(request, 'register.html',)


class LogoutView(View):

    def get(self, request):
        logout(request)
        return render(request, 'logout.html')


class SettingsView(View):

    def get(self, request):
        user = request.user
        # form = UserForm()
        context = {
            'user': user,
            # 'form': form,
        }
        return render(request, 'settings.html', context)

    def post(self, request):

        form_name = request.POST.get('form_name')

        if form_name == 'add_category':
            Category.objects.create(name=request.POST.get('category'))
            return redirect('settings')

        if form_name == 'edit_user':
            user = request.user
            user.first_name = request.POST.get('first_name')
            user.save()
            return redirect('settings')
