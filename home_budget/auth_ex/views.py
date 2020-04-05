from django.contrib import (
    messages,
)
from django.contrib.auth import (
    get_user_model,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from django.urls import (
    reverse_lazy,
)
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
from auth_ex.forms import (
    AddCategoryForm,
    EditUserForm,
    CustomUserCreationForm,
    UploadFileForm,
)
from budget.models import (
    Category,
    Expenses,
    Income
)
from home_budget.functions import (
    file_handler,
)
User = get_user_model()


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('auth_ex:login')
    template_name = 'auth_ex/register.html'

    def form_valid(self, form):
        user = form.save()
        categories = Category.objects.filter(default_category=True)
        user.categories.set(categories)
        return super().form_valid(form)


class SettingsView(LoginRequiredMixin, View):

    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        user_form = EditUserForm(initial={
            'username': user.username,
            'email': user.email,
            'send_email': user.send_email,
        })
        add_category_form = AddCategoryForm()
        upload_file_form = UploadFileForm()
        context = {
            'add_category_form': add_category_form,
            'user': user,
            'user_form': user_form,
            'upload_file_form': upload_file_form,
        }

        return render(request, 'auth_ex/settings.html', context)

    def post(self, request):

        form_name = request.POST.get('form_name')

        if form_name == 'add_category':
            user = User.objects.get(pk=request.user.id)
            add_category_form = AddCategoryForm(request.POST)
            if add_category_form.is_valid():
                try:
                    category = Category.objects.get(
                        name__iexact=add_category_form.cleaned_data['name']
                    )
                except Category.DoesNotExist:
                    category = Category.objects.create(
                        name=add_category_form.cleaned_data['name'],
                        default_category=False
                    )
                user.categories.add(category)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Pomyślnie dodano kategorię"
                )
            return redirect('auth_ex:settings')

        if form_name == 'edit_user':
            user_form = EditUserForm(request.POST)
            if user_form.is_valid():
                user = User.objects.get(pk=request.user.id)
                user.email = user_form.cleaned_data['email']
                user.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Pomyślnie zmieniono dane",
                )

        if form_name == "upload_file":
            file_form = UploadFileForm(request.POST, request.FILES)
            if file_form.is_valid():
                data = file_handler(request.FILES['file'])
                for expense in data[0]:

                    try:
                        category = Category.objects.get(name__iexact=expense['category'])
                    except Category.DoesNotExist:
                        category = Category.objects.create(
                            name=expense['category'],
                            default_category=False
                        )
                    Expenses.objects.create(
                        date=expense['expense_date'],
                        category=category,
                        amount=expense['expense_amount'],
                        comment=expense['expense_comment'],
                        user=request.user,
                    )
                for income in data[1]:
                    Income.objects.create(
                        date=income['income_date'],
                        amount=income['income_amount'],
                        comment=income['income_comment'],
                        user=request.user,
                    )

                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Pomyślnie wczytano dane",
                )
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Błąd wczytywania danych",
                )

        return redirect('auth_ex:settings')


class SignOutCategory(LoginRequiredMixin, View):

    def post(self, request, category_id):
        user = User.objects.get(pk=request.user.id)
        user.categories.remove(Category.objects.get(pk=category_id))
        return redirect('auth_ex:settings')


class SignInCategory(LoginRequiredMixin, View):

    def post(self, request, category_id):
        user = User.objects.get(pk=request.user.id)
        user.categories.add(Category.objects.get(pk=category_id))
        return redirect('auth_ex:settings')


class StatuteView(TemplateView):
    template_name = 'auth_ex/statute.html'
