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

        month = request.GET.get('month', datetime.date.today().month)
        total_income = sum([income.amount for income in Income.objects.filter(user=request.user).filter(date__month=month)])
        total_expenses = sum([expense.amount for expense in Expenses.objects.filter(user=request.user).filter(date__month=month)])
        total_savings = total_income - total_expenses

        context = {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'total_savings': total_savings,
        }
        return render(request, 'index.html', context)


class ExpensesView(LoginRequiredMixin, View):

    def get(self, request):

        month = request.GET.get('month', datetime.date.today().month)
        year = request.GET.get('year', datetime.date.today().year)
        category = request.GET.get('category', 1)

        print(category)

        categories = Category.objects.order_by('name')
        expenses = Expenses.objects.filter(user=request.user).filter(date__year=year).filter(date__month=month).\
            filter(category=Category.objects.get(pk=category)).order_by('-date')
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

        month = request.GET.get('month', datetime.date.today().month)
        year = request.GET.get('year', datetime.date.today().year)

        incomes = Income.objects.filter(user=request.user).filter(date__year=year).filter(date__month=month).order_by('date')

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
