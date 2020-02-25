from django.contrib.auth.forms import (
    UserCreationForm,
)
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
from django.views.generic import (
    DetailView,
)
from budget.models import (
    Category,
)
from users.forms import (
    EditUserForm,
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
            user.last_name = request.POST.get('last_name')            
            user.save()
            return redirect('settings')


class UserView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'users/user-detail.html'
    pk_url_kwarg = 'user_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EditUserForm
        return context