from rest_framework import serializers
from budget.models import (
    Category,
    Expenses,
    Income,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = ['date', 'category', 'amount', 'comment']


class IncomeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Income
        fields = [
            # 'url',
            'date',
            'amount',
            'comment'
        ]
