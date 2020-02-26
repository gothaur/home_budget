from budget.forms import (
    AddExpenseForm,
    AddIncomeForm,
)


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
    expense_form = AddExpenseForm()
    income_form = AddIncomeForm()
    context = {
        'expense_form': expense_form,
        'income_form': income_form,
    }
    return context
