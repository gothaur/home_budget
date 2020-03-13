from django import forms
from django.utils import timezone
from budget.models import (
    Category,
    Income,
)


class AddExpenseForm(forms.Form):
    date = forms.DateField()
    amount = forms.DecimalField(
        decimal_places=2,
        max_digits=10,
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.order_by('name'),
    )
    comment = forms.CharField(
        required=False,
        max_length=255,
        label='Komentarz',
    )


# class AddIncomeForm(forms.Form):
#     date = forms.DateField(
#         widget=forms.DateInput(
#             attrs={
#                 'class': 'form-control mb-2 mr-sm-2',
#                 'type': 'date',
#             }
#         ),
#         label='Data',
#         initial=timezone.datetime.today().strftime('%Y-%m-%d'),
#     )
#     date.input_type = 'date'
#     amount = forms.DecimalField(
#         widget=forms.NumberInput(
#             attrs={
#                 'class': 'form-control mb-2 mr-sm-2',
#             }
#         ),
#         label='Kwota',
#         decimal_places=2,
#         max_digits=10,
#     )
#     comment = forms.CharField(
#         widget=forms.Textarea(
#             attrs={
#                 'class': 'form-control mb-2 mr-sm-2',
#                 'rows': 2,
#             }
#         ),
#         required=False,
#         max_length=255,
#         label='Komentarz',
#     )


class AddIncomeForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control mb-2 mr-sm-2',
            }
        ),
        label='Data',
    )
    amount = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control mb-2 mr-sm-2',
            }
        ),
        label='Kwota',
        decimal_places=2,
        max_digits=10,
    )
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control mb-2 mr-sm-2',
                'rows': 2,
            }
        ),
        required=False,
        max_length=255,
        label='Komentarz',
    )

    class Meta:
        model = Income
        fields = [
            'date',
            'amount',
            'comment',
        ]


class FilterExpensesForm(forms.Form):
    date_from = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control mb-2 mr-sm-2',
                'type': 'date',
            }
        ),
        label='Od',
        required=False,
        initial=timezone.localdate(),
    )
    date_from.input_type = 'date'
    date_to = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control mb-2 mr-sm-2',
                'type': 'date',
            }
        ),
        label='Do',
        required=False,
    )
    date_to.input_type = 'date'
    category = forms.ModelChoiceField(
        queryset=Category.objects.order_by('name'),
        widget=forms.Select(
            attrs={
                'class': 'form-control mb-2 mr-sm-2',
            }
        ),
        label='Kategoria',
        required=False,
    )
