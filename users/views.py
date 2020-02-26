from django.contrib.auth.forms import (
    UserCreationForm,
)
from django.shortcuts import (
    render,
    redirect,
)
from django.views import (
    View,
)
from users.forms import (
    EditUserForm,
)
from budget.models import (
    Category,
)


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


class SettingsView(View):

    def get(self, request):
        user = request.user
        user_form = EditUserForm(initial={
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        })
        context = {
            'user': user,
            'user_form': user_form,
        }
        return render(request, 'settings.html', context)

    def post(self, request):

        form_name = request.POST.get('form_name')
        
        if form_name == 'add_category':
            Category.objects.create(name=request.POST.get('category'))
            return redirect('settings')

        if form_name == 'edit_user':
            user_form = EditUserForm(request.POST)
            if user_form.is_valid():
                user = request.user
                user.first_name = user_form.cleaned_data['first_name']
                user.last_name = user_form.cleaned_data['last_name']
                user.email = user_form.cleaned_data['email']
                user.save()

        return redirect('settings')
