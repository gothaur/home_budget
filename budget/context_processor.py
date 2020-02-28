from django.contrib.auth.models import (
    User,
)
from budget.forms import (
    AddExpenseForm,
    AddIncomeForm,
)
from budget.models import (
    Category,
)


def sidebars(request):
    if request.path == '/expenses/':
        message = "expenses"
    elif request.path == '/income/':
        message = "income"
    elif request.path == '/summary/':
        message = "summary"
    elif request.path == '/users/edit/':
        message = "settings"
    else:
        message = None
    return {'message': message}


def add_entry_form(request):
    expense_form = AddExpenseForm()
    income_form = AddIncomeForm(
        initial={
            'user': request.user.username,
        }
    )
    user = User.objects.get(pk=request.user.id)
    user_categories = user.profile.categories.order_by('name')
    all_categories = Category.objects.exclude(
        name__in=[category.name for category in user_categories]
    )
    context = {
        'expense_form': expense_form,
        'income_form': income_form,
        'all_categories': all_categories,
        'user_categories': user_categories,
    }
    return context
