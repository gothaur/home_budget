from datetime import datetime

from django.contrib.auth import (
    authenticate,
    login,
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
from django.urls import reverse_lazy
from django.utils import (
    timezone,
)
from django.views import (
    View,
)
from django.views.generic import (
    DeleteView,
)
from home_budget.functions import (
    data_filter,
    get_month_names,
)
from budget.forms import (
    AddExpenseForm,
    FilterExpensesForm,
)
from budget.models import (
    Expenses,
    Income,
)


class Index(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('users:login')
        else:
            return redirect('expenses')

    def post(self, request):

        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            request.session['username'] = user.username
            return redirect('summary')

        return redirect('users:login')


class ExpensesView(LoginRequiredMixin, View):

    def get(self, request):
        date_from = request.GET.get("date_from", timezone.localdate())
        date_to = request.GET.get("date_to", timezone.localdate())
        selected_category = request.GET.get("category", "-1")
        expenses = data_filter(request, Expenses, date_from, date_to, selected_category)

        user = User.objects.get(pk=request.user.id)
        categories = user.profile.categories.order_by('name')

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

            Expenses.objects.create(date=date, category=category,
                                    amount=amount, comment=comment, user=request.user)

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
        date_from = request.GET.get("date_from", timezone.localdate())
        date_to = request.GET.get("date_to", timezone.localdate())
        total_income = sum([income.amount for income in data_filter(request, Income, date_from, date_to)])
        total_expenses = sum([expense.amount for expense in data_filter(request, Expenses, date_from, date_to)])
        total_savings = total_income - total_expenses

        months = get_month_names()
        user = User.objects.get(pk=request.user.id)
        categories = [category.name for category in user.profile.categories.order_by('name')]

        result = []

        for i, category in enumerate(categories):
            result.append([])
            for month in range(1, 13):
                monthly_amount = 0
                for expense in Expenses.objects.filter(user=request.user).filter(category__name=category) \
                        .filter(date__year=timezone.now().year).filter(date__month=month):
                    monthly_amount += expense.amount
                result[i].append(monthly_amount)

        context = {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'total_savings': total_savings,
            'months': months,
            'categories': categories,
            'result': result,
            'date_from': date_from,
            'date_to': date_to,
        }
        return render(request, 'summary.html', context)


class DeleteExpense(LoginRequiredMixin, View):

    def post(self, request, expense_id):
        Expenses.objects.get(pk=expense_id).delete()
        return redirect('expenses')


class DeleteExpenseView(LoginRequiredMixin, DeleteView):
    http_method_names = ['post']
    model = Expenses
    pk_url_kwarg = 'expense_id'
    success_url = reverse_lazy('expenses')


class DeleteIncomeView(LoginRequiredMixin, DeleteView):
    http_method_names = ['post']
    model = Income
    pk_url_kwarg = 'income_id'
    success_url = reverse_lazy('income')
