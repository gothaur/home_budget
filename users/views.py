from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from django.contrib.auth.forms import UserCreationForm
# from django.http import HttpResponseRedirect
from django.shortcuts import (
    render,
    redirect,
)
from django.views import View
from users.forms import (
    UserForm,
)


class LoginView(View):

    def get(self, request):
        logout(request)
        return render(request, 'login.html')

    def post(self, request):

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            # if user.is_active():
            login(request, user)
            request.session['username'] = username
            return redirect('index')

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


class LogoutView(View):

    def get(self, request):
        logout(request)
        return render(request, 'logout.html')


class EditView(View):

    def get(self, request):
        user = request.user
        form = UserForm()
        context = {
            'user': user,
            'form': form,
        }
        return render(request, 'edit.html', context)
