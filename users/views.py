from django.contrib import (
    messages,
)
from django.contrib.auth.forms import (
    UserCreationForm,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from django.contrib.auth.models import (
    User,
)
from django.shortcuts import (
    redirect,
    render,
)
from django.views import (
    View,
)
from budget.models import (
    Category,
)
from users.forms import (
    AddCategoryForm,
    EditUserForm,
)
from users.models import (
    Profile,
)


class RegisterView(View):

    def get(self, request):
        form = UserCreationForm()
        context = {
            'form': form,
        }
        return render(request, 'users/register.html', context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            categories = Category.objects.filter(
                default_category=True,
            )
            user = form.save()
            profile = Profile(
                user=user,
            )
            profile.save()
            profile.categories.set(categories)
            return redirect('users:login')
        else:
            context = {
                'form': form,
            }
            return render(
                request,
                'users/register.html',
                context,
            )


class SettingsView(View):

    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        user_form = EditUserForm(initial={
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        })
        add_category_form = AddCategoryForm()
        context = {
            'add_category_form': add_category_form,
            'user': user,
            'user_form': user_form,
        }
        return render(request, 'users/settings.html', context)

    def post(self, request):

        form_name = request.POST.get('form_name')

        if form_name == 'add_category':
            if Category.objects.filter(name__iexact=request.POST.get('name')).exists():
                messages.add_message(
                    request,
                    messages.WARNING,
                    "Taka kategoria już istnieje",
                )
            else:
                user = User.objects.get(pk=request.user.id)
                add_category_form = AddCategoryForm(request.POST)
                if add_category_form.is_valid():
                    category = Category.objects.create(
                        name=add_category_form.cleaned_data['name'],
                        default_category=False)
                    user.profile.categories.add(category)
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        "Pomyślnie dodano nową kategorię",
                    )
            return redirect('users:settings')

        if form_name == 'edit_user':
            user_form = EditUserForm(request.POST)
            if user_form.is_valid():
                user = User.objects.get(pk=request.user.id)
                user.first_name = user_form.cleaned_data['first_name']
                user.last_name = user_form.cleaned_data['last_name']
                user.email = user_form.cleaned_data['email']
                user.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Pomyślnie zmieniono dane",
                )

        return redirect('users:settings')


class SignOutCategory(LoginRequiredMixin, View):

    def post(self, request, category_id):
        user = User.objects.get(pk=request.user.id)
        user.profile.categories.remove(Category.objects.get(pk=category_id))
        return redirect('users:settings')


class SignInCategory(LoginRequiredMixin, View):

    def post(self, request, category_id):
        user = User.objects.get(pk=request.user.id)
        user.profile.categories.add(Category.objects.get(pk=category_id))
        return redirect('users:settings')
