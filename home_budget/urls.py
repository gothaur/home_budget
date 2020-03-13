"""home_budget URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import (
    path,
    include,
)
from budget import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    # path('add-category/', views.AddCategory.as_view(), name='add-category'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api'),),
    path('expense/delete/<int:expense_id>/', views.DeleteExpenseView.as_view(), name='delete-expense'),
    path('expenses/', views.ExpensesView.as_view(), name='expenses'),
    path('income/', views.IncomeView.as_view(), name='income'),
    path('income/delete/<int:income_id>/', views.DeleteIncomeView.as_view(), name='delete-income'),
    path('income/edit/<int:income_id>/', views.EditIncomeView.as_view(), name='edit-income'),
    path('summary/', views.Summary.as_view(), name='summary'),
    path('users/', include('auth_ex.urls',  namespace='auth_ex'),),
]
