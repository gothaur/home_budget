import os
from datetime import (
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
from django.core.mail import (
    send_mail,
)
from django.db.models import (
    Sum,
    Value,
)
from django.db.models.functions import (
    Coalesce,
)
from django.db.models.functions import (
    TruncMonth,
)
from django.http import (
    FileResponse,
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
    Expenses,
    Income,
)
from home_budget.functions import (
    monthly_report,
)
from home_budget.settings import BASE_DIR

User = get_user_model()


class Index(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'welcome-page.html')

        user = request.user

        try:
            ex = Expenses.objects.filter(
                    user=user,
                ).order_by('date')[0].date
        except IndexError:
            ex = timezone.now().date()

        try:
            inc = Income.objects.filter(
                    user=user,
                ).order_by('date')[0].date
        except IndexError:
            inc = timezone.now().date()

        rd = relativedelta(
            datetime(
                timezone.now().year,
                timezone.now().month,
                1,
            ),
            min(
                inc,
                ex
            ),
        )
        number_of_months = rd.years * 12 + rd.months

        dates = [
                    datetime(
                        timezone.now().year,
                        timezone.now().month,
                        1,
                    ).date() - relativedelta(
                        months=i
                    ) for i in range(number_of_months + 1)
                ][::-1]

        monthly_income_set = Income.objects.filter(
            user=user,
        ).annotate(
            month=TruncMonth('date'),
        ).values(
            'month',
        ).annotate(date_sum=Sum('amount')).order_by('month')

        monthly_expenses_set = Expenses.objects.filter(
            user=user,
        ).annotate(
            month=TruncMonth('date'),
        ).values(
            'month',
        ).annotate(date_sum=Sum('amount')).order_by('month')

        monthly_expenses_sum = []
        monthly_income_sum = []
        monthly_total_savings_list = []
        monthly_total_savings = 0

        for date in dates:
            income = monthly_income_set.filter(
                date__month=date.month,
                date__year=date.year,
            ).aggregate(
                result=Coalesce(
                    Sum('amount'),
                    Value(0)
                )
            )['result']
            monthly_income_sum.append(
                income or 0
            )

            expense = monthly_expenses_set.filter(
                date__month=date.month,
                date__year=date.year,
            ).aggregate(
                result=Coalesce(
                    Sum('amount'),
                    Value(0)
                )
            )['result']
            monthly_expenses_sum.append(
                expense or 0
            )
            monthly_total_savings += (income or 0) - (expense or 0)
            monthly_total_savings_list.append(monthly_total_savings)

        my_style = Style(
            colors=(
                'green',
                '#d10f25',
            )
        )
        expense_income_chart = pygal.Bar(
            style=my_style,
            show_legend=True,
            legend_at_bottom=True,
            x_label_rotation=45,
            no_data_text="Brak danych",

        )
        expense_income_chart.force_uri_protocol = 'https'
        expense_income_chart.title = 'Miesięczne przychody oraz wydatki [w PLN]'
        expense_income_chart.x_labels = dates
        expense_income_chart.add(
            'Przychody',
            monthly_income_sum,
            color='green',
        )
        expense_income_chart.add(
            'Wydatki',
            monthly_expenses_sum,
        )

        total_balance_chart = pygal.Line(
            style=Style(
                colors=(
                    'blue',
                    'red',
                    'green',
                )
            ),
            x_label_rotation=45,
            show_legend=True,
            legend_at_bottom=True,
            no_data_text="Brak danych"
        )

        total_balance_chart.force_uri_protocol = 'https'
        total_balance_chart.title = 'Przyrost oszczędności [w PLN]'
        total_balance_chart.x_labels = dates
        total_balance_chart.add(
            'Oszczędności',
            monthly_total_savings_list
        )
        total_balance_chart.add(
            'Wydatki',
            [(-expense) for expense in monthly_expenses_sum]
        )
        total_balance_chart.add(
            'Przychody',
            [income for income in monthly_income_sum]
        )
        total_balance_chart = total_balance_chart.render_data_uri()

        monthly_income_expense_chart = expense_income_chart.render_data_uri()

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
            'income_chart': monthly_income_expense_chart,
            'expenses_chart': expenses_result,
            'total_balance_chart': total_balance_chart,
        }

        return render(request, 'chart.html', context)


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

    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        from_date_to_render = 11
        total_income_value = Income.objects.filter(
            user_id=user.id,
        ).aggregate(
            amount_sum=Coalesce(
                Sum('amount'),
                Value(0),
            ))
        total_expenses_value = Expenses.objects.filter(
            user_id=user.id,
        ).aggregate(
            amount_sum=Coalesce(
                Sum('amount'),
                Value(0),
            ))
        total_savings = total_income_value['amount_sum'] - total_expenses_value['amount_sum']

        dates = [
                    datetime(
                        timezone.now().year,
                        timezone.now().month,
                        1,
                    ).date() - relativedelta(
                        months=i
                    ) for i in range(from_date_to_render + 1)
                ][::-1]

        categories = user.categories.order_by('name')

        result = []

        for i, category in enumerate(categories):
            result.append([])
            for month in dates:
                monthly_amount = Expenses.objects.filter(
                    user=request.user,
                    category__name=category.name,
                    date__year=month.year,
                    date__month=month.month
                ).aggregate(
                    amount_sum=Coalesce(
                        Sum('amount'),
                        Value(0),
                    ))['amount_sum']
                result[i].append(monthly_amount)

        monthly_income = []
        monthly_expenses = []
        sigma = []

        for date in dates:
            income = Income.objects.filter(
                user_id=user.id,
                date__year=date.year,
                date__month=date.month,
            ).aggregate(
                amount_sum=Coalesce(
                    Sum('amount'),
                    Value(0),
                ))['amount_sum']
            monthly_income.append(income)
            expense = Expenses.objects.filter(
                user_id=user.id,
                date__year=date.year,
                date__month=date.month,
            ).aggregate(
                amount_sum=Coalesce(
                    Sum('amount'),
                    Value(0),
                ))['amount_sum']
            monthly_expenses.append(expense)
            sigma.append(income - expense)

        context = {
            'months': dates,
            'categories': categories,
            'result': result,
            'monthly_income': monthly_income,
            'monthly_expenses': monthly_expenses,
            'total_savings': total_savings,
            'sigma': sigma,
        }
        return render(request, 'summary.html', context)


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


class GenerateReportView(LoginRequiredMixin, View):

    def get(self, request):

        user = request.user
        date = datetime(
            timezone.now().year,
            timezone.now().month,
            1
        )

        categorized_expenses = Expenses.objects.filter(
            user=user,
            date__gte=date,
        ).values(
            'category__name',
        ).order_by(
            'category__name',
        ).annotate(
            total_sum=Sum('amount')
        )
        income = Income.objects.filter(
            user=user,
            date__gte=date
        ).aggregate(
            total=Coalesce(
                Sum('amount'),
                Value(0),
            )
        )['total']
        expenses = Expenses.objects.filter(
            user=user,
            date__gte=date
        ).aggregate(
            total=Coalesce(
                Sum('amount'),
                Value(0),
            )
        )['total']
        result = monthly_report(
            date.strftime('%Y-%m'),
            income,
            expenses,
            categorized_expenses,
        )
        report = {
            'to': user.email,
            'subject': f"Raport z {date.strftime('%Y-%m')}",
            'content': result,
        }

        context = {
            'message': 'Błąd wysyłania raportu. Upewnij się, że został podany poprawny adres e-mail'
        }

        if user.email:
            send_mail(
                report['subject'],
                report['content'],
                'raport@zaplanuj.budzet.pl',
                [user.email],
                fail_silently=False,
            )
            context = {
                'message': 'Raport wysłany',
            }

        return render(request, 'send-report.html', context)


class ManualFileView(View):

    def get(self, request):
        return FileResponse(
            open(os.path.join(BASE_DIR, 'media/documentation.pdf'), 'rb'),
            # content_type='application/pdf'
        )
