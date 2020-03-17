from django.contrib.auth import (
    get_user_model,
)
from django.db.models import (
    Sum,
)
from rest_framework import viewsets
# from rest_framework.authentication import (
#     SessionAuthentication,
#     BasicAuthentication,
# )

from api.serializers import (
    CategorySerializer,
    ExpensesSerializer,
    IncomeSerializer,
)

from budget.models import (
#     Category,
    Expenses,
    Income,
)
User = get_user_model()


class IncomeViewSet(
    viewsets.ModelViewSet,
):
    """
    API endpoint that allows incomes to be viewed.
    """
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = IncomeSerializer

    def get_queryset(self):
        user = User.objects.get(username=self.kwargs.get('user_name'))
        self.queryset = Income.objects.filter(user=user).order_by('date')
        # self.queryset = Income.objects.order_by('date')
        # return super().get_queryset()
        return self.queryset

# Members.objects.values('designation').annotate(dcount=Count('designation'))


class ExpenseViewSet(
    viewsets.ModelViewSet,
):
    """
    API endpoint that allows groups to be viewed.
    """
    serializer_class = ExpensesSerializer

    def get_queryset(self):
        user = User.objects.get(username=self.kwargs.get('user_name'))
        self.queryset = Expenses.objects.filter(user=user).order_by('date').aggregate()
        return self.queryset

    # def get_queryset(self):
    #     user = User.objects.get(username=self.kwargs.get('user_name'))
    #     self.queryset = Expenses.objects.values('category__name').annotate(cat_sum=Sum('amount'))
    #     print(self.queryset)
    #     return self.queryset
