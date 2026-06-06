from django.urls import path
from . import views

urlpatterns = [
    path('', views.finance_dashboard, name='finance_dashboard'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/create/', views.transaction_create, name='transaction_create'),
    path('transactions/<int:pk>/', views.transaction_detail, name='transaction_detail'),
    # Pledges removed (Change 6)
    path('report/', views.financial_report, name='financial_report'),
    path('report/download/', views.financial_report_download, name='financial_report_download'),
]
