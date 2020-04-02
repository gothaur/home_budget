from __future__ import absolute_import, unicode_literals

from datetime import datetime

from celery import shared_task
from django.contrib.auth import (
    get_user_model,
)
from django.core.mail import (
    send_mail,
)
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
from django.utils import timezone

from budget.models import (
    Expenses,
    Income,
)
from home_budget.functions import monthly_report

User = get_user_model()


@shared_task
def print_message_to_console():
    send_mail(
        'subject',
        'content',
        'raport@zaplanuj.budzet.pl',
        ['bartynski.michal@gmail.com'],
        fail_silently=False,
    )


@shared_task
def email_monthly_report():
    for user in User.objects.all():
        if user.email:
            date = datetime(
                timezone.now().year,
                timezone.now().month - 1,
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
                'subject': f"Raport z {date.strftime('%Y-%m')}",
                'content': result,
            }

            if user.email:
                send_mail(
                    report['subject'],
                    report['content'],
                    'raport@zaplanuj.budzet.pl',
                    [user.email],
                    fail_silently=False,
                )
