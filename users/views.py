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
        context = {
            'user': user,
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
            user.last_name = request.POST.get('last_name')            
            user.save()
            return redirect('settings')
