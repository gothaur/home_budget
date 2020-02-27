from django.contrib import (
    messages,
)
from django.contrib.auth.forms import (
    UserCreationForm,
)
from django.db import (
    IntegrityError,
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
from users.forms import (
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
        return render(request, 'register.html', context)

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
            try:
                category = Category.objects.create(
                    name=request.POST.get('category'),
                    default_category=False,
                )
            except IntegrityError:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Taka kategoria już istnieje",
                )
                return redirect('users:settings')
            user = request.user
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
                user = request.user
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
