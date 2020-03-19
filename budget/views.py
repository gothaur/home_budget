from datetime import (
    date,
    datetime,
)
from dateutil.relativedelta import (
    relativedelta,
)
import pygal
from pygal.style import (
    LightColorizedStyle as LCS,
    LightenStyle as LS,
    Style,
)
from django.contrib.auth import (
    get_user_model,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from django.db.models import (
    Q,
    Sum,
    Value,
)
from django.db.models.functions import (
    Coalesce,
)
from django.db.models.functions import (
    TruncMonth,
)
from django.shortcuts import (
    redirect,
    render,
)
from django.urls import reverse_lazy
from django.utils import (
    timezone,
)
from django.views import (
    View,
)
from django.views.generic import (
    DeleteView,
    DetailView,
    UpdateView,
)
from home_budget.functions import (
    data_filter,
)
from budget.forms import (
    AddExpenseForm,
    AddIncomeForm,
)
from budget.models import (
    Category,
    Expenses,
    Income,
)
User = get_user_model()


class Index(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'welcome-page.html')

        user = request.user
        monthly_incomes_list = Income.objects.filter(
            user=user,
        ).annotate(
            month=TruncMonth('date'),
        ).values(
            'month',
        ).annotate(date_sum=Sum('amount')).order_by('month')
        dates, monthly_income_sum = [], []
        for income in monthly_incomes_list:
            dates.append(income['month'].strftime('%Y-%m'))
            monthly_income_sum.append(
                {
                    'value': float(income['date_sum']),
                    'color': 'green',
                }
            )

        monthly_expenses_list = Expenses.objects.filter(
            user=user,
        ).annotate(
            month=TruncMonth('date'),
        ).values(
            'month',
        ).annotate(date_sum=Sum('amount')).order_by('month')
        monthly_expenses_sum = []
        for expenses in monthly_expenses_list:
            monthly_expenses_sum.append(
                {
                    'value': float(expenses['date_sum']),
                    'color': 'red',
                }
            )
        my_style = Style(
            colors=(
                'green',
                # 'red',
                '#d10f25',
            )
        )
        income_chart = pygal.HorizontalBar(
            # fill=True,
            style=my_style,
            # x_label_rotation=45,
            # interpolate='cubic',
            show_legend=True,
            legend_at_bottom=True,
            no_data_text="Brak danych",

        )
        income_chart.force_uri_protocol = 'https'
        income_chart.title = 'Miesięczne przychody [w PLN]'
        income_chart.x_labels = dates
        income_chart.add(
            'Przychody',
            monthly_income_sum,
            color='green',
        )
        income_chart.add(
            'Wydatki',
            monthly_expenses_sum,
        )

        monthly_savings_chart = income_chart.render_data_uri()

        expenses_category, expenses_amount = [], []
        expenses_list = Expenses.objects.filter(
            user=user,
        ).values(
            'category__name',
        ).annotate(cat_sum=Sum('amount')).order_by('-cat_sum')
        for expense in expenses_list:
            expenses_category.append(expense['category__name'])
            expenses_amount.append(float(expense['cat_sum']))
        my_style = LS(
            '#333366',
            base_style=LCS,
        )
        expenses_chart = pygal.Bar(
            style=my_style,
            x_label_rotation=45,
            show_legend=False,
            no_data_text="Brak danych",
        )
        expenses_chart.force_uri_protocol = 'https'
        expenses_chart.title = 'Wydatki wg kategorii [w PLN]'
        expenses_chart.x_labels = expenses_category
        expenses_chart.add('', expenses_amount)
        expenses_result = expenses_chart.render_data_uri()

        context = {
            'income_chart': monthly_savings_chart,
            'expenses_chart': expenses_result,
        }

        return render(
            request, 'chart.html',
            context,
        )


class ExpensesView(LoginRequiredMixin, View):

    def get(self, request):
        date_from = request.GET.get("date_from", timezone.localdate())
        date_to = request.GET.get("date_to", timezone.localdate())
        selected_category = request.GET.get("category", "-1")
        expenses = data_filter(request, Expenses, date_from, date_to, selected_category)

        user = User.objects.get(pk=request.user.id)
        categories = user.categories.order_by('name')

        context = {
            'categories': categories,
            'expenses': expenses,
            'date_from': date_from,
            'date_to': date_to,
            'today': timezone.localdate().strftime('%Y-%m-%d'),
        }
        return render(request, 'expenses.html', context)

    def post(self, request):
        form = AddExpenseForm(
            request.POST,
        )

        if form.is_valid():
            date = form.cleaned_data['date']
            category = form.cleaned_data['category']
            amount = form.cleaned_data['amount']
            comment = form.cleaned_data['comment']

            Expenses.objects.create(
                date=date,
                category=category,
                amount=amount,
                comment=comment,
                user=request.user
            )

        return redirect('expenses')


class IncomeView(LoginRequiredMixin, View):

    def get(self, request):
        date_from = request.GET.get("date_from", timezone.localdate())
        date_to = request.GET.get("date_to", timezone.localdate())
        incomes = data_filter(request, Income, date_from, date_to)
        context = {
            'incomes': incomes,
            'date_from': date_from,
            'date_to': date_to,
        }
        return render(request, 'income.html', context)

    def post(self, request):
        date = request.POST.get('date')
        amount = request.POST.get('amount')
        comment = request.POST.get('comment')

        Income.objects.create(date=date, amount=amount, comment=comment, user=request.user)

        return redirect('income')


class Summary(LoginRequiredMixin, View):

    # def get(self, request):
    #     # user = User.objects.get(pk=request.user.id)
    #     # date_from = request.GET.get("date_from", timezone.localdate())
    #     # date_to = request.GET.get("date_to", timezone.localdate())
    #     # total_income = data_filter(
    #     #     request,
    #     #     Income,
    #     #     date_from,
    #     #     date_to,
    #     # ).aggregate(Sum('amount'))['amount__sum']
    #     # total_income = total_income or 0
    #     # total_expenses = data_filter(
    #     #     request,
    #     #     Expenses,
    #     #     date_from,
    #     #     date_to,
    #     # ).aggregate(Sum('amount'))['amount__sum']
    #     # total_expenses = total_expenses or 0
    #     # savings = total_income - total_expenses
    #     # income = Income.objects.filter(
    #     #     user_id=user.id,
    #     # ).aggregate(
    #     #     Sum('amount')
    #     # )['amount__sum'] or 0
    #     # expenses = Expenses.objects.filter(
    #     #     user_id=user.id,
    #     # ).aggregate(
    #     #     Sum('amount')
    #     # )['amount__sum'] or 0
    #     # total_savings = income - expenses
    #     #
    #     # months = get_month_names()
    #     # categories = user.categories.order_by('name')
    #     #
    #     # result = []
    #     #
    #     # for i, category in enumerate(categories):
    #     #     result.append([])
    #     #     for month in range(1, 13):
    #     #         monthly_amount = Expenses.objects.filter(
    #     #             user=request.user,
    #     #             category__name=category.name,
    #     #             date__year=timezone.now().year,
    #     #             date__month=month).aggregate(Sum('amount'))['amount__sum']
    #     #         result[i].append(monthly_amount if monthly_amount is not None else 0)
    #     #
    #     # monthly_income = []
    #     # monthly_expenses = []
    #     # sigma = []
    #     #
    #     # for month in range(1, 13):
    #     #     income = Income.objects.filter(
    #     #         user_id=user.id,
    #     #         date__year=timezone.now().year,
    #     #         date__month=month,
    #     #     ).aggregate(Sum('amount'))['amount__sum']
    #     #     monthly_income.append(
    #     #         income if income is not None else 0
    #     #     )
    #     #     expense = Expenses.objects.filter(
    #     #         user_id=user.id,
    #     #         date__year=timezone.now().year,
    #     #         date__month=month,
    #     #     ).aggregate(Sum('amount'))['amount__sum']
    #     #     monthly_expenses.append(
    #     #         expense if expense is not None else 0
    #     #     )
    #     #
    #     #     sigma.append(monthly_income[month - 1] - monthly_expenses[month - 1])
    #     #
    #     # context = {
    #     #     'total_income': total_income,
    #     #     'total_expenses': total_expenses,
    #     #     'savings': savings,
    #     #     'months': months,
    #     #     'categories': categories,
    #     #     'result': result,
    #     #     'date_from': date_from,
    #     #     'date_to': date_to,
    #     #     'monthly_income': monthly_income,
    #     #     'monthly_expenses': monthly_expenses,
    #     #     'total_savings': total_savings,
    #     #     'sigma': sigma,
    #     # }
    #
    #     user = request.user
    #     expenses_set = Expenses.objects.filter(
    #         user=user,
    #         date__gte=date.today() - relativedelta(months=5),
    #     ).annotate(
    #         month=TruncMonth('date'),
    #     ).values(
    #         'month',
    #         'category__name',
    #     ).annotate(
    #         date_sum=Sum('amount')
    #     ).order_by('month')
    #
    #     categories = Category.objects.filter(user=user).order_by('name')
    #
    #     label_dates, dates, expenses_by_category = [], [], []
    #     for expense in expenses_set:
    #         label_dates.append(expense['month'].strftime('%Y-%m'))
    #         dates.append(expense['month'])
    #         expenses_by_category.append(
    #             {
    #                 'value': float(expense['date_sum']),
    #                 'label': expense['category__name'],
    #             }
    #         )
    #
    #     income_chart = pygal.Bar(
    #         show_legend=True,
    #         legend_at_bottom=True,
    #         no_data_text="Brak danych",
    #     )
    #     # income_chart.force_uri_protocol = 'https'
    #     # income_chart.title = 'Miesięczne wydatki [w PLN]'
    #     # tmp = []
    #     # dates = list(dict.fromkeys(dates))
    #     # income_chart.x_labels = dates
    #
    #     # for i, category in enumerate(categories):
    #     #     tmp.append([])
    #     #     for j, exp in enumerate(expenses_set):
    #     #         if category.name == exp['category__name']:
    #     #             tmp[i].append(expenses_by_category[j])
    #     #
    #     #
    #     # for t in tmp:
    #     #     if len(t) > 0:
    #     #         income_chart.add(
    #     #             t[0]['label'],
    #     #             # '',
    #     #             t,
    #     #         )
    #
    #     income_chart.force_uri_protocol = 'https'
    #     income_chart.title = 'Miesięczne wydatki [w PLN]'
    #     tmp = {}
    #     dates = list(dict.fromkeys(dates))
    #     label_dates = list(dict.fromkeys(label_dates))
    #     income_chart.x_labels = label_dates
    #
    #     for category in categories:
    #         tmp[category.name] = []
    #         for month in dates:
    #             try:
    #                 elem = expenses_set.get(
    #                     Q(
    #                         category__name=category.name
    #                     ) & Q(
    #                         month=month
    #                     )
    #                 )
    #             except Expenses.DoesNotExist:
    #                 elem = {
    #                     'category__name': category.name,
    #                     'month': month,
    #                     'date_sum': 0
    #                 }
    #             tmp[category.name].append(
    #                 {
    #                     'value': elem['date_sum'],
    #                     'label': elem['category__name'],
    #                 }
    #             )
    #
    #     for t in tmp.values():
    #         if len(t) > 0:
    #             income_chart.add(
    #                 t[0]['label'],
    #                 t,
    #             )
    #
    #     income_result = income_chart.render_data_uri()
    #     # income_result = income_chart.render_table(
    #     #     style=True,
    #     #     total=True,
    #     #     transpose=True,
    #     # )
    #     context = {
    #         'result': income_result,
    #         # 'result': ExpensesTable(Expenses.objects.all()),
    #     }
    #     return render(request, 'summary-chart.html', context)
    #     # return render(request, 'summary.html', context)

    # def get(self, request):
    #
    #     user = request.user
    #     expenses_set = Expenses.objects.filter(
    #         user=user,
    #         date__gte=date.today() - relativedelta(months=5),
    #     ).annotate(
    #         month=TruncMonth('date'),
    #     ).values(
    #         'month',
    #         'category__name',
    #     ).annotate(
    #         date_sum=Sum('amount')
    #     ).order_by('month')
    #
    #     categories = Category.objects.filter(user=user).order_by('name')
    #
    #     label_dates, dates, expenses_by_category = [], [], []
    #     for expense in expenses_set:
    #         label_dates.append(expense['month'].strftime('%Y-%m'))
    #         dates.append(expense['month'])
    #         expenses_by_category.append(
    #             {
    #                 'value': float(expense['date_sum']),
    #                 'label': expense['category__name'],
    #             }
    #         )
    #
    #     income_chart = pygal.Bar(
    #         show_legend=True,
    #         legend_at_bottom=True,
    #         no_data_text="Brak danych",
    #     )
    #
    #     income_chart.force_uri_protocol = 'https'
    #     income_chart.title = 'Miesięczne wydatki [w PLN]'
    #     tmp = {}
    #     dates = list(dict.fromkeys(dates))
    #     label_dates = list(dict.fromkeys(label_dates))
    #     income_chart.x_labels = label_dates
    #
    #     for category in categories:
    #         tmp[category.name] = []
    #         for month in dates:
    #             try:
    #                 elem = expenses_set.get(
    #                     Q(
    #                         category__name=category.name
    #                     ) & Q(
    #                         month=month
    #                     )
    #                 )
    #             except Expenses.DoesNotExist:
    #                 elem = {
    #                     'category__name': category.name,
    #                     'month': month,
    #                     'date_sum': 0
    #                 }
    #             tmp[category.name].append(
    #                 {
    #                     'value': elem['date_sum'],
    #                     'label': elem['category__name'],
    #                 }
    #             )
    #
    #     for t in tmp.values():
    #         if len(t) > 0:
    #             income_chart.add(
    #                 t[0]['label'],
    #                 t,
    #             )
    #
    #     income_result = income_chart.render_data_uri()
    #     # income_result = income_chart.render_table(
    #     #     style=True,
    #     #     total=True,
    #     #     transpose=True,
    #     # )
    #     context = {
    #         'result': income_result,
    #     }
    #     return render(request, 'summary-chart.html', context)

    def get(self, request):

        user = request.user
        expenses_set = Expenses.objects.filter(
            user=user,
            date__gte=datetime(datetime.now().year, datetime.now().month, 1) - relativedelta(months=8),
        ).annotate(
            month=TruncMonth('date'),
        ).values(
            'month',
            'category__name',
        ).annotate(
            date_sum=Sum('amount'),
        ).order_by('month')

        monthly_expenses = [
            expense['month_sum'] for expense in expenses_set.values(
                'month'
            ).annotate(
                month_sum=Coalesce(
                    Sum('amount'),
                    Value(0)
                )
            )
        ]

        categories = Category.objects.filter(user=user).order_by('name')

        label_dates, dates, expenses_by_category = [], [], []
        for expense in expenses_set:
            label_dates.append(expense['month'].strftime('%Y-%m'))
            dates.append(expense['month'])
            expenses_by_category.append(
                {
                    'value': float(expense['date_sum']),
                    'label': expense['category__name'],
                }
            )

        expenses_table = pygal.Bar(
            show_legend=True,
            legend_at_bottom=True,
            no_data_text="Brak danych",
            margin_bottom=50,
        )

        expenses_table.force_uri_protocol = 'https'
        expenses_table.title = 'Miesięczne wydatki [w PLN]'
        tmp = {}
        dates = list(dict.fromkeys(dates))
        label_dates = list(dict.fromkeys(label_dates))
        expenses_table.x_labels = label_dates

        for category in categories:
            tmp[category.name] = []
            for month in dates:
                try:
                    elem = expenses_set.get(
                        Q(
                            category__name=category.name
                        ) & Q(
                            month=month
                        )
                    )
                except Expenses.DoesNotExist:
                    elem = {
                        'category__name': category.name,
                        'month': month,
                        'date_sum': 0
                    }
                tmp[category.name].append(
                    {
                        'value': elem['date_sum'],
                        'label': elem['category__name'],
                    }
                )

        for t in tmp.values():
            if len(t) > 0:
                expenses_table.add(
                    t[0]['label'],
                    t,
                )

        expenses_table.add(
            'WYDATKI',
            monthly_expenses,
        )

        monthly_incomes_list = Income.objects.filter(
            user=user,
            date__gte=datetime(datetime.now().year, datetime.now().month, 1) - relativedelta(months=8),
        ).annotate(
            month=TruncMonth('date'),
        ).values(
            'month',
        ).annotate(date_sum=Sum('amount')).order_by('month')
        balance, monthly_income = [], []
        for i, income in enumerate(monthly_incomes_list):
            monthly_income.append(
                {
                    'value': float(income['date_sum']),
                    'color': 'green',
                }
            )
            balance.append(income['date_sum'] - monthly_expenses[i])

        expenses_table.add(
            'PRZYCHODY',
            monthly_income,
        )
        expenses_table.add(
            'SALDO',
            balance,
        )

        # income_result = income_chart.render_data_uri()
        income_result = expenses_table.render_table(
            style=True,
            # total=True,
            transpose=True,
        )
        context = {
            'result': income_result,
            'total_savings': Income.objects.filter(
                user=user,
            ).aggregate(
                total_sum=Sum('amount')
            )['total_sum'] - Expenses.objects.filter(
                user=user,
            ).aggregate(
                total_sum=Sum('amount')
            )['total_sum']
        }
        return render(request, 'summary-chart.html', context)


class DeleteExpenseView(LoginRequiredMixin, DeleteView):
    """
    delete expense from list
    """
    http_method_names = ['post']
    model = Expenses
    pk_url_kwarg = 'expense_id'
    success_url = reverse_lazy('expenses')


class DeleteIncomeView(LoginRequiredMixin, DeleteView):
    """
    delete income from list
    """
    http_method_names = ['post']
    model = Income
    pk_url_kwarg = 'income_id'
    success_url = reverse_lazy('income')


class EditIncomeView(LoginRequiredMixin, UpdateView):
    form_class = AddIncomeForm
    model = Income
    pk_url_kwarg = 'income_id'
    success_url = reverse_lazy('income')
    template_name = 'edit-income.html'


class EditExpenseView(LoginRequiredMixin, UpdateView):
    form_class = AddExpenseForm
    model = Expenses
    pk_url_kwarg = 'expense_id'
    success_url = reverse_lazy('expenses')
    template_name = 'edit-expense.html'


class IncomeDetailView(LoginRequiredMixin, DetailView):
    model = Income
    pk_url_kwarg = 'income_id'
    template_name = 'income-detail.html'
