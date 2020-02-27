from django import forms
from django.contrib.auth.models import (
    User,
)
from django.utils import timezone
from budget.models import (
    Category,
)


class AddExpenseForm(forms.Form):

    def __init__(self, filter_on, *args, **kwargs):
        super(AddExpenseForm, self).__init__(*args, **kwargs)
        self.fields['category'] = forms.ModelChoiceField(
            queryset=Category.objects.filter(profile__user__username=filter_on).order_by('name'),
            widget=forms.Select(
                attrs={
                    'class': 'form-control mb-2 mr-sm-2',
                }
            ),
            label='Kategoria',
        )

    user = forms.CharField(
        widget=forms.HiddenInput(
        ),
        required=False,
    )
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control mb-2 mr-sm-2',
                'type': 'date',
            }
        ),
        label='Data',
        initial=timezone.datetime.today().strftime('%Y-%m-%d'),
    )
    amount = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control mb-2 mr-sm-2',
            }
        ),
        label='Kwota',
        decimal_places=2,
        max_digits=8,
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(profile__user__username=user).order_by('name'),
        # queryset=Category.objects.order_by('name'),
        # widget=forms.Select(
        #     attrs={
        #         'class': 'form-control mb-2 mr-sm-2',
        #     }
        # ),
        # label='Kategoria',
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


class AddIncomeForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control mb-2 mr-sm-2',
                'type': 'date',
            }
        ),
        label='Data',
        initial=timezone.datetime.today().strftime('%Y-%m-%d'),
    )
    date.input_type = 'date'
    amount = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control mb-2 mr-sm-2',
            }
        ),
        label='Kwota',
        decimal_places=2,
        max_digits=8,
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
