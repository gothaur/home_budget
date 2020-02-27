from django.urls import (
    path,
)
from api import views

app_name = 'api'

urlpatterns = [
    path('expenses/', views.ExpensesList.as_view(), name='api-expenses'),
    path('income/', views.IncomeList.as_view(), name='api-income'),
    path('expense/<int:id>/', views.ExpenseView.as_view(), name='expense-detail'),
    path('income/<int:id>/', views.IncomeView.as_view(), name='income-detail'),
    path('categories/', views.CategoriesList.as_view(), name='categories'),
]
