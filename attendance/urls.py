from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance_list, name='attendance_list'),
    path('create/', views.attendance_create, name='attendance_create'),
    path('<int:pk>/', views.attendance_detail, name='attendance_detail'),
    path('analytics/', views.attendance_analytics, name='attendance_analytics'),
]
