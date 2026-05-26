from django.urls import path
from . import views

urlpatterns = [
    path('', views.finance_dashboard, name='finance_dashboard'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/create/', views.transaction_create, name='transaction_create'),
    path('transactions/<int:pk>/', views.transaction_detail, name='transaction_detail'),
    path('pledges/', views.pledge_list, name='pledge_list'),
    path('pledges/create/', views.pledge_create, name='pledge_create'),
    path('report/', views.financial_report, name='financial_report'),
]
