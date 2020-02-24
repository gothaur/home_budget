# from django.contrib.auth import (
#     authenticate,
#     login,
#     logout,
# )
from django.contrib.auth.forms import (
    UserCreationForm,
)
# from django.contrib.auth.views import (
#     LoginView,
# )
from django.shortcuts import (
    render,
    redirect,
)
# from django.urls import reverse_lazy
from django.views import (
    View,
)
from budget.models import (
    Category,
)

# from users.forms import (
#     LoginForm,
# )
#
#
# class MyLoginView(View):
#
#     def get(self, request):
#         logout(request)
#         ctx = {
#             'form': LoginForm()
#         }
#         return render(
#             request,
#             'login.html',
#             ctx,
#         )
#
#     def post(self, request):
#
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
#             if user is not None:
#                 # if user.is_active():
#                 login(request, user)
#                 request.session['username'] = user.username
#                 return redirect(request.GET.get('next', '/'))
#
#         return redirect('login')


# class MyLoginView(LoginView):
#
#     success_url = reverse_lazy('index')


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
            return render(
                request,
                'register.html',
                context,
            )


# class LogoutView(View):
#
#     def get(self, request):
#         logout(request)
#         return render(request, 'logout.html')


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
