from django.contrib.auth import (
    get_user_model,
)
from django.utils import (
    timezone,
)
from budget.forms import (
    AddExpenseForm,
    AddIncomeForm,
    FilterExpensesForm,
)
from budget.models import (
    Category,
)
User = get_user_model()


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
    income_form = AddIncomeForm()
    user_categories = []
    all_categories = []
    try:
        user = User.objects.get(pk=request.user.id)
        user_categories = user.categories.order_by('name')
        all_categories = Category.objects.exclude(
            name__in=[category.name for category in user_categories]
        )
    except:
        pass
    context = {
        'expense_form': expense_form,
        'income_form': income_form,
        'all_categories': all_categories,
        'user_categories': user_categories,
    }
    return context


def filter_forms(request):
    expense_filter_form = FilterExpensesForm()

    context = {
        'expense_filter_form': expense_filter_form,
    }
    return context


def date(request):
    context = {
        'month': timezone.localdate(),
    }
    return context


def version(request):
    context = {
        'version': '0.94 beta',
        'today': timezone.datetime.today().strftime('%Y-%m-%d'),
    }
    return context
