import calendar
import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
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


class Index(View):

    def get(self, request):
        return render(request, 'index.html')


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


class Summary(LoginRequiredMixin, View):

    def get(self, request):
        date_from = request.GET.get("date_from", "")
        date_to = request.GET.get("date_to", "")
        total_income = sum([income.amount for income in dataFilter(request, Income, date_from, date_to)])
        total_expenses = sum([expense.amount for expense in dataFilter(request, Expenses, date_from, date_to)])
        total_savings = total_income - total_expenses
        categories = Category.objects.order_by('name')

        months = []
        monthly_expenses = []
        annual_expenses = []

        for i in range(1, 13):
            months.append(calendar.month_name[i])

        # annual_income = []
        #         annual_expenses = []
        #         annual_savings = []
        #         months = []
        #
        #         for month in range(1, 13):
        #             months.append(datetime.datetime(current_year, month, 1).strftime('%B'))
        #             total_income = sum([income.amount for income in Income.objects.filter(user=request.user)
        #                                .filter(date__month=month)])
        #             total_expenses = sum([expense.amount for expense in Expenses.objects.
        #                                  filter(user=request.user).filter(date__month=month)])
        #             savings = total_income - total_expenses
        #             annual_income.append(total_income)
        #             annual_expenses.append(total_expenses)
        #             annual_savings.append(savings)
        #
        #         total_costs = zip(annual_income, annual_expenses, annual_savings, months)

        for i in range(1, 13):
            annual_expenses.append([])
            for category in categories:
                annual_expenses[i - 1].append(sum([expense.amount for expense in Expenses.objects.
                                              filter(user=request.user).filter(category=category)
                                              .filter(date__month=i)]))

        for i in range(len(annual_expenses)):
            annual_expenses[i] = sum(annual_expenses[i])

        data = zip(categories, annual_expenses)

        context = {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'total_savings': total_savings,
            'categories': categories,
            'months': months,
            'data': data,
        }
        return render(request, 'summary.html', context)
