import pygal
from pygal.style import (
    LightColorizedStyle as LCS,
    LightenStyle as LS,
)
from django.contrib.auth import (
    get_user_model,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from django.db.models import (
    Sum,
)
from django.db.models.functions import (
    TruncMonth,
    TruncYear,
)
from django.shortcuts import (
    redirect,
    render,
)
from django.urls import reverse_lazy
from django.utils import (
    timezone,
)
from django.views import (
    View,
)
from django.views.generic import (
    DeleteView,
    DetailView,
    UpdateView,
)
from home_budget.functions import (
    data_filter,
    get_month_names,
)
from budget.forms import (
    AddExpenseForm,
    AddIncomeForm,
)
from budget.models import (
    Expenses,
    Income,
)
User = get_user_model()


class Index(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'welcome-page.html')

        # income_url = f"http://127.0.0.1:8000/api/{request.user.username}/api-income/"
        # # url = reverse("api:Income-list")
        # # url = reverse("income", request=request)
        # # url = "http://127.0.0.1:8000/api/income/"
        # # url = "https://api.github.com/search/repositories?q=language:python&sort=stars"
        # requested_income = requests.get(income_url)
        #
        # response_income_list = requested_income.json()
        user = request.user
        income_list = Income.objects.filter(
            user=user,
        ).annotate(
            month=TruncMonth('date'),
        ).values(
            'month',
        ).annotate(date_sum=Sum('amount')).order_by('month')
        income_date, income_amount = [], []
        for income in income_list:
            income_date.append(income['month'].strftime('%Y-%m'))
            income_amount.append(float(income['date_sum']))
        my_style = LS('#333366', base_style=LCS)
        income_chart = pygal.Bar(
            style=my_style,
            x_label_rotation=45,
            show_legend=False,
        )
        income_chart.force_uri_protocol = 'https'
        income_chart.title = 'Miesięczne przychody [w PLN]'
        income_chart.x_labels = income_date
        income_chart.add('', income_amount)
        income_result = income_chart.render_data_uri()

        expenses_category, expenses_amount = [], []
        expenses_list = Expenses.objects.filter(
            user=user,
        ).values(
            'category__name',
        ).annotate(cat_sum=Sum('amount')).order_by('-cat_sum')
        for expense in expenses_list:
            expenses_category.append(expense['category__name'])
            expenses_amount.append(float(expense['cat_sum']))
        expenses_chart = pygal.Bar(
            style=my_style,
            x_label_rotation=45,
            show_legend=False,
        )
        expenses_chart.force_uri_protocol = 'https'
        expenses_chart.title = 'Wydatki wg kategorii [w PLN]'
        expenses_chart.x_labels = expenses_category
        expenses_chart.add('', expenses_amount)
        expenses_result = expenses_chart.render_data_uri()

        context = {
            'income_chart': income_result,
            'expenses_chart': expenses_result,
        }

        return render(
            request, 'chart.html',
            context,
        )


class ExpensesView(LoginRequiredMixin, View):

    def get(self, request):
        date_from = request.GET.get("date_from", timezone.localdate())
        date_to = request.GET.get("date_to", timezone.localdate())
        selected_category = request.GET.get("category", "-1")
        expenses = data_filter(request, Expenses, date_from, date_to, selected_category)

        user = User.objects.get(pk=request.user.id)
        categories = user.categories.order_by('name')

        context = {
            'categories': categories,
            'expenses': expenses,
            'date_from': date_from,
            'date_to': date_to,
            'today': timezone.localdate().strftime('%Y-%m-%d'),
        }
        return render(request, 'expenses.html', context)

    def post(self, request):
        form = AddExpenseForm(
            request.POST,
        )

        if form.is_valid():
            date = form.cleaned_data['date']
            category = form.cleaned_data['category']
            amount = form.cleaned_data['amount']
            comment = form.cleaned_data['comment']

            Expenses.objects.create(
                date=date,
                category=category,
                amount=amount,
                comment=comment,
                user=request.user
            )

        return redirect('expenses')


class IncomeView(LoginRequiredMixin, View):

    def get(self, request):
        date_from = request.GET.get("date_from", timezone.localdate())
        date_to = request.GET.get("date_to", timezone.localdate())
        incomes = data_filter(request, Income, date_from, date_to)
        context = {
            'incomes': incomes,
            'date_from': date_from,
            'date_to': date_to,
        }
        return render(request, 'income.html', context)

    def post(self, request):
        date = request.POST.get('date')
        amount = request.POST.get('amount')
        comment = request.POST.get('comment')

        Income.objects.create(date=date, amount=amount, comment=comment, user=request.user)

        return redirect('income')


class Summary(LoginRequiredMixin, View):

    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        date_from = request.GET.get("date_from", timezone.localdate())
        date_to = request.GET.get("date_to", timezone.localdate())
        total_income = data_filter(
            request,
            Income,
            date_from,
            date_to,
        ).aggregate(Sum('amount'))['amount__sum']
        total_income = total_income or 0
        total_expenses = data_filter(
            request,
            Expenses,
            date_from,
            date_to,
        ).aggregate(Sum('amount'))['amount__sum']
        total_expenses = total_expenses or 0
        savings = total_income - total_expenses
        income = Income.objects.filter(
            user_id=user.id,
        ).aggregate(
            Sum('amount')
        )['amount__sum'] or 0
        expenses = Expenses.objects.filter(
            user_id=user.id,
        ).aggregate(
            Sum('amount')
        )['amount__sum'] or 0
        total_savings = income - expenses

        months = get_month_names()
        categories = user.categories.order_by('name')

        result = []

        for i, category in enumerate(categories):
            result.append([])
            for month in range(1, 13):
                monthly_amount = Expenses.objects.filter(
                    user=request.user,
                    category__name=category.name,
                    date__year=timezone.now().year,
                    date__month=month).aggregate(Sum('amount'))['amount__sum']
                result[i].append(monthly_amount if monthly_amount is not None else 0)

        monthly_income = []
        monthly_expenses = []
        sigma = []

        for month in range(1, 13):
            income = Income.objects.filter(
                user_id=user.id,
                date__year=timezone.now().year,
                date__month=month,
            ).aggregate(Sum('amount'))['amount__sum']
            monthly_income.append(
                income if income is not None else 0
            )
            expense = Expenses.objects.filter(
                user_id=user.id,
                date__year=timezone.now().year,
                date__month=month,
            ).aggregate(Sum('amount'))['amount__sum']
            monthly_expenses.append(
                expense if expense is not None else 0
            )

            sigma.append(monthly_income[month - 1] - monthly_expenses[month - 1])

        context = {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'savings': savings,
            'months': months,
            'categories': categories,
            'result': result,
            'date_from': date_from,
            'date_to': date_to,
            'monthly_income': monthly_income,
            'monthly_expenses': monthly_expenses,
            'total_savings': total_savings,
            'sigma': sigma,
        }
        return render(request, 'summary.html', context)


class DeleteExpenseView(LoginRequiredMixin, DeleteView):
    """
    delete expense from list
    """
    http_method_names = ['post']
    model = Expenses
    pk_url_kwarg = 'expense_id'
    success_url = reverse_lazy('expenses')


class DeleteIncomeView(LoginRequiredMixin, DeleteView):
    """
    delete income from list
    """
    http_method_names = ['post']
    model = Income
    pk_url_kwarg = 'income_id'
    success_url = reverse_lazy('income')


class EditIncomeView(LoginRequiredMixin, UpdateView):
    form_class = AddIncomeForm
    model = Income
    pk_url_kwarg = 'income_id'
    success_url = reverse_lazy('income')
    template_name = 'edit-income.html'


class EditExpenseView(LoginRequiredMixin, UpdateView):
    form_class = AddExpenseForm
    model = Expenses
    pk_url_kwarg = 'expense_id'
    success_url = reverse_lazy('expenses')
    template_name = 'edit-expense.html'


class IncomeDetailView(LoginRequiredMixin, DetailView):
    model = Income
    pk_url_kwarg = 'income_id'
    template_name = 'income-detail.html'
