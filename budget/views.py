from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import (
    render,
    redirect,
)
from django.views import View
from home_budget.functions import (
    data_filter,
    get_month_names,
)
from budget.models import (
    Category,
    Expenses,
    Income,
)


# class Index(View):
#
#     def get(self, request):
#         return render(request, 'index.html')


class Index(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        else:
            return redirect('expenses')

    def post(self, request):

        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            request.session['username'] = user.username
            return redirect('summary')

        return redirect('login')


class ExpensesView(LoginRequiredMixin, View):

    def get(self, request):
        date_from = request.GET.get("date_from", "")
        date_to = request.GET.get("date_to", "")
        selected_category = request.GET.get("selected_category", "-1")
        expenses = data_filter(request, Expenses, date_from, date_to, selected_category)

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
        incomes = data_filter(request, Income, date_from, date_to)
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
        total_income = sum([income.amount for income in data_filter(request, Income, date_from, date_to)])
        total_expenses = sum([expense.amount for expense in data_filter(request, Expenses, date_from, date_to)])
        total_savings = total_income - total_expenses

        months = get_month_names()
        categories = [category.name for category in Category.objects.order_by('name')]

        result = []

        for i, category in enumerate(categories):
            result.append([])
            for month in range(1,13):
                monthly_amount = 0
                for expense in Expenses.objects.filter(user=request.user).filter(category__name=category).filter(date__month=month):
                    monthly_amount += expense.amount
                result[i].append(monthly_amount)

        context = {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'total_savings': total_savings,
            'months': months,
            'categories': categories,
            'result': result
        }
        return render(request, 'summary.html', context)
