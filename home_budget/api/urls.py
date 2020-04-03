from django.urls import (
    include,
    path,
)
from rest_framework import routers
from api import views

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'api-income',
                views.IncomeViewSet,
                basename='api-income',
                )
router.register(r'api-expenses',
                views.ExpenseViewSet,
                basename='api-expenses',
                )

urlpatterns = [
    path(
        '<str:user_name>/',
        include(
            (
                router.urls,
                'api',
            ),
            namespace='api-income',
        )
    ),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

# urlpatterns = [
#     #  path('expenses/', views.ExpensesList.as_view(), name='api-expenses'),
#     path('income/', views.IncomeViewSet.as_view(), name='api-income'),
#     #  path('expense/<int:id>/', views.ExpenseView.as_view(), name='expense-detail'),
#     #  path('income/<int:id>/', views.IncomeView.as_view(), name='income-detail'),
#     #  path('categories/', views.CategoriesList.as_view(), name='categories'),
# ]
