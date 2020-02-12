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


class Index(View):

    def get(self, request):

        total_income = sum([income.amount for income in Income.objects.all()])
        total_expenses = sum([expense.amount for expense in Expenses.objects.all()])
        savings = total_income - total_expenses

        context = {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'savings': savings,
        }
        return render(request, 'index.html', context)


class ExpensesView(View):

    def get(self, request):

        categories = Category.objects.order_by('name')
        expenses = Expenses.objects.order_by('date')

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

        Expenses.objects.create(date=date, category=Category.objects.get(pk=category), amount=amount, comment=comment)

        return redirect('expenses')


class IncomeView(View):

    def get(self, request):

        incomes = Income.objects.order_by('date')

        context = {
            'incomes': incomes,
        }
        return render(request, 'income.html', context)

    def post(self, request):
        date = request.POST.get('date')
        amount = request.POST.get('amount')
        comment = request.POST.get('comment')

        Income.objects.create(date=date, amount=amount, comment=comment)

        return redirect('income')


class AddCategory(View):

    def get(self, request):
        return render(request, 'add-category.html')

    def post(self, request):
        name = request.POST.get('name')
        Category.objects.create(name=name)
        return redirect('index')
