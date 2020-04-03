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
    category = serializers.StringRelatedField()

    class Meta:
        model = Expenses
        fields = [
            'date',
            'category',
            'amount',
            'comment',
            'user',
        ]


# class IncomeSerializer(serializers.HyperlinkedModelSerializer):
class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = [
            'date',
            'amount',
            'comment',
            'user',
        ]
