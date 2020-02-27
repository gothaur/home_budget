from budget.forms import (
    AddExpenseForm,
    AddIncomeForm,
)
from budget.models import Category


def sidebars(request):
    if request.path == '/expenses/':
        message = "expenses"
    elif request.path == '/income/':
        message = "income"
    elif request.path == '/summary/':
        message = "summary"
    else:
        message = None
    return {'message': message}


def add_entry_form(request):
    expense_form = AddExpenseForm(
        # initial={
        #     'user': request.user.username,
        #     'category': Category.objects.filter(profile__user__username=request.user.username).order_by('name'),
        # }
        filter_on=request.user.username,
    )
    income_form = AddIncomeForm(
        initial={
            'user': request.user.username,
        }
    )
    context = {
        'expense_form': expense_form,
        'income_form': income_form,
    }
    return context
