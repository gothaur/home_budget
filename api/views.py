# from django.contrib.auth import (
#     get_user_model,
# )
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.http import (
#     Http404,
#     JsonResponse,
# )
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from budget.models import (
#     Category,
#     Expenses,
#     Income,
# )
# from api.serializers import (
#     CategorySerializer,
#     ExpensesSerializer,
#     IncomeSerializer,
# )
# User = get_user_model()
#
#
# class ExpensesList(LoginRequiredMixin, APIView):
#
#     def get(self, request, format=None):
#         expenses = Expenses.objects.filter(user=request.user)
#         serializer = ExpensesSerializer(expenses, many=True, context={"request": request})
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = ExpensesSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class IncomeList(LoginRequiredMixin, APIView):
#
#     def get(self, request, format=None):
#         income = Income.objects.filter(user=request.user)
#         serializer = IncomeSerializer(
#             income,
#             many=True,
#             context={"request": request}
#         )
#
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = IncomeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class CategoriesList(APIView):
#
#     def get(self, request, format=None):
#         category = Category.objects.filter(user=request.user)
#         serializer = CategorySerializer(category, many=True, context={"request": request})
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = CategorySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class ExpenseView(APIView):
#
#     def get_object(self, pk):
#         try:
#             return Expenses.objects.get(pk=pk)
#         except Expenses.DoesNotExist:
#             raise Http404
#
#     def get(self, request, id, format=None):
#         expense = self.get_object(id)
#         serializer = ExpensesSerializer(expense, context={"request": request})
#         return Response(serializer.data)
#
#     def delete(self, request, id, format=None):
#         expense = self.get_object(id)
#         expense.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#     def put(self, request, id, format=None):
#         expense = self.get_object(id)
#         serializer = ExpensesSerializer(expense, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def post(self, request, id, format=None):
#         pass
#
#
# class IncomeView(APIView):
#
#     def get_object(self, pk):
#         try:
#             return Income.objects.get(pk=pk)
#         except Income.DoesNotExist:
#             raise Http404
#
#     def get(self, request, id, format=None):
#         income = self.get_object(id)
#         serializer = IncomeSerializer(income, context={"request": request})
#         return Response(serializer.data)
#
#     def delete(self, request, id, format=None):
#         income = self.get_object(id)
#         income.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#     def put(self, request, id, format=None):
#         income = self.get_object(id)
#         serializer = IncomeSerializer(income, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def post(self, request, id, format=None):
#         pass


from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions

from api.serializers import (
    CategorySerializer,
    ExpensesSerializer,
    IncomeSerializer,
)

from budget.models import (
#     Category,
#     Expenses,
    Income,
)


class IncomeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = IncomeSerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Income.objects.order_by('date')

    # def get_queryset(self):
    #     self.queryset = Income.objects.filter(user=self.request.user)
    #     return self.queryset


# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]
