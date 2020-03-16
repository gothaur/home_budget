from django.urls import (
    include,
    path,
)
from rest_framework import routers
from api import views

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'api-income', views.IncomeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

# urlpatterns = [
#     path('expenses/', views.ExpensesList.as_view(), name='api-expenses'),
#     path('income/', views.IncomeList.as_view(), name='api-income'),
#     path('expense/<int:id>/', views.ExpenseView.as_view(), name='expense-detail'),
#     path('income/<int:id>/', views.IncomeView.as_view(), name='income-detail'),
#     path('categories/', views.CategoriesList.as_view(), name='categories'),
# ]
