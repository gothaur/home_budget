from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import (
    render,
    redirect,
)
from django.views import View
from budget.functions import (
    dataFilter,
)
from budget.models import (
    Category,
    Expenses,
    Income,
)
import datetime
import calendar


class Index(LoginRequiredMixin, View):

    def get(self, request):
        
        date_from = request.GET.get("date_from", "")
        date_to = request.GET.get("date_to", "")
        total_income = sum([income.amount for income in dataFilter(request, Income, date_from, date_to)])
        total_expenses = sum([expense.amount for expense in dataFilter(request, Expenses, date_from, date_to)])
        total_savings = total_income - total_expenses

        context = {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'total_savings': total_savings,
        }
        return render(request, 'index.html', context)


class ExpensesView(LoginRequiredMixin, View):

    def get(self, request):
        
        date_from = request.GET.get("date_from", "")
        date_to = request.GET.get("date_to", "")
        selected_category = request.GET.get("selected_category", "-1")
        expenses = dataFilter(request, Expenses, date_from, date_to, selected_category)

        categories = Category.objects.order_by('name')

        context = {
            'categories': categories,
            'expenses': expenses,
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

        date_from = request.GET.get("date_from", "")
        date_to = request.GET.get("date_to", "")

        # month = request.GET.get('month', datetime.date.today().month)
        # year = request.GET.get('year', datetime.date.today().year)

        # incomes = Income.objects.filter(user=request.user).filter(date__year=year).filter(date__month=month).order_by('date')
        incomes = dataFilter(request, Income, date_from, date_to)
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
