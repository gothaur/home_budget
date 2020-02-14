from django.shortcuts import (
    render,
    redirect,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views import View
from budget.models import (
    Category,
    Expenses,
    Income,
)
from budget.serializers import (
    ExpensesSerializer,
    IncomeSerializer,
)


class Index(View):

    def get(self, request):

        total_income = sum([income.amount for income in Income.objects.all()])
        total_expenses = sum([expense.amount for expense in Expenses.objects.all()])
        savings = total_income - total_expenses

        context = {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'savings': savings,
        }
        return render(request, 'index.html', context)


class ExpensesView(View):

    def get(self, request):

        categories = Category.objects.order_by('name')
        expenses = Expenses.objects.order_by('date')
        partial_expenses = []

        for category in categories:
            category_sum = 0
            for expense in expenses:
                if expense.category == category:
                    category_sum += expense.amount
            partial_expenses.append(category_sum)

        data = zip(partial_expenses, categories)

        context = {
            'categories': categories,
            'expenses': expenses,
            'partial_expenses': partial_expenses,
            "data": data,
        }
        return render(request, 'expenses.html', context)

    def post(self, request):
        date = request.POST.get('date')
        category = request.POST.get('category')
        amount = request.POST.get('amount')
        comment = request.POST.get('comment')

        Expenses.objects.create(date=date, category=Category.objects.get(pk=category), amount=amount, comment=comment)

        return redirect('expenses')


class IncomeView(View):

    def get(self, request):

        incomes = Income.objects.order_by('date')

        context = {
            'incomes': incomes,
        }
        return render(request, 'income.html', context)

    def post(self, request):
        date = request.POST.get('date')
        amount = request.POST.get('amount')
        comment = request.POST.get('comment')

        Income.objects.create(date=date, amount=amount, comment=comment)

        return redirect('income')


class AddCategory(View):

    def get(self, request):
        return render(request, 'add-category.html')

    def post(self, request):
        name = request.POST.get('name')
        Category.objects.create(name=name)
        return redirect('index')


class ExpensesList(APIView):

    def get(self, request, format=None):
        expenses = Expenses.objects.all()
        serializer = ExpensesSerializer(expenses, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ExpensesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IncomeList(APIView):

    def get(self, request, format=None):
        income = Income.objects.all()
        serializer = IncomeSerializer(income, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = IncomeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class BookView(APIView):
#
#     def get_object(self, pk):
#         try:
#             return Book.objects.get(pk=pk)
#         except Book.DoesNotExist:
#             raise Http404
#
#     def get(self, request, id, format=None):
#         book = self.get_object(id)
#         serializer = BookSerializer(book, context={"request": request})
#         return Response(serializer.data)
#
#     def delete(self, request, id, format=None):
#         book = self.get_object(id)
#         book.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#     def put(self, request, id, format=None):
#         book = self.get_object(id)
#         serializer = BookSerializer(book, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def post(self, request, id, format=None):
#         pass
