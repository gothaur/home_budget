from django.contrib import (
    messages,
)
from django.contrib.auth import (
    get_user_model,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
)
from django.shortcuts import (
    redirect,
    render,
)
from django.views import (
    View,
)
from django.views.generic import (
    TemplateView,
)
from budget.models import (
    Category,
)
from users.forms import (
    AddCategoryForm,
    EditUserForm,
    CustomUserCreationForm
)
User = get_user_model()


# class RegisterView(View):
#
#     def get(self, request):
#         form = CustomUserCreationForm()
#         context = {
#             'form': form,
#         }
#         return render(request, 'users/register.html', context)
#
#     def post(self, request):
#         form = CustomUserCreationForm(request.POST)
#
#         if form.is_valid():
#             categories = Category.objects.filter(
#                 default_category=True,
#             )
#             user = form.save()
#             user.categories.set(categories)
#             return redirect('users:login')
#         else:
#             context = {
#                 'form': form,
#             }
#             return render(
#                 request,
#                 'users/register.html',
#                 context,
#             )


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        user = form.save()
        categories = Category.objects.filter(default_category=True)
        user.categories.set(categories)
        user.save()
        return super().form_valid(form)


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
                    user.categories.add(category)
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
        user.categories.remove(Category.objects.get(pk=category_id))
        return redirect('users:settings')


class SignInCategory(LoginRequiredMixin, View):

    def post(self, request, category_id):
        user = User.objects.get(pk=request.user.id)
        user.categories.add(Category.objects.get(pk=category_id))
        return redirect('users:settings')


class StatuteView(TemplateView):
    template_name = 'users/statute.html'
