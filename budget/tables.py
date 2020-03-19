from django_tables2 import tables
from budget.models import (
    Expenses
)


class ExpensesTable(tables.Table):
    class Meta:
        model = Expenses
