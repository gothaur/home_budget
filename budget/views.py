from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import (
    render,
    redirect,
)
from django.views import View
from budget.models import (
    Category,
    Expenses,
    Income,
)
import datetime


class Index(LoginRequiredMixin, View):

    def get(self, request):
        
        current_year = datetime.date.today().year
        annual_income = []
        annual_expenses = []
        annual_savings = []
        months = []

        for month in range(1, 13):
            months.append(datetime.datetime(current_year, month, 1).strftime('%B'))
            total_income = sum([income.amount for income in Income.objects.filter(user=request.user)
                               .filter(date__month=month)])
            total_expenses = sum([expense.amount for expense in Expenses.objects.
                                 filter(user=request.user).filter(date__month=month)])
            savings = total_income - total_expenses
            annual_income.append(total_income)
            annual_expenses.append(total_expenses)
            annual_savings.append(savings)

        total_costs = zip(annual_income, annual_expenses, annual_savings, months)

        context = {
            'total_costs': total_costs,
        }
        return render(request, 'index.html', context)


class ExpensesView(LoginRequiredMixin, View):

    def get(self, request):

        categories = Category.objects.order_by('name')
        expenses = Expenses.objects.filter(user=request.user).order_by('date')
        partial_expenses = []

        for category in categories:
            category_sum = 0
            for expense in expenses:
                if expense.category == category:
                    category_sum += expense.amount
            partial_expenses.append(category_sum)

        data = zip(partial_expenses, categories)

        context = {
            'categories': categories,
            'expenses': expenses,
            'partial_expenses': partial_expenses,
            "data": data,
        }
        return render(request, 'expenses.html', context)

    def post(self, request):
        date = request.POST.get('date')
        category = request.POST.get('category')
        amount = request.POST.get('amount')
        comment = request.POST.get('comment')

        Expenses.objects.create(date=date, category=Category.objects.get(pk=category),
                                amount=amount, comment=comment, user=request.user)

        return redirect('expenses')


class IncomeView(LoginRequiredMixin, View):

    def get(self, request):

        incomes = Income.objects.filter(user=request.user).order_by('date')

        context = {
            'incomes': incomes,
        }
        return render(request, 'income.html', context)

    def post(self, request):
        date = request.POST.get('date')
        amount = request.POST.get('amount')
        comment = request.POST.get('comment')

        Income.objects.create(date=date, amount=amount, comment=comment, user=request.user)

        return redirect('income')


class AddCategory(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'add-category.html')

    def post(self, request):
        name = request.POST.get('name')
        Category.objects.create(name=name)
        return redirect('index')
