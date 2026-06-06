from django.urls import path
from . import views

urlpatterns = [
    path('', views.member_list, name='member_list'),
    path('create/', views.member_create, name='member_create'),
    path('<int:pk>/', views.member_detail, name='member_detail'),
    path('<int:pk>/edit/', views.member_edit, name='member_edit'),
    path('<int:pk>/delete/', views.member_delete, name='member_delete'),
    # Families removed (Change 1)
    path('visitors/', views.visitor_list, name='visitor_list'),
    path('visitors/create/', views.visitor_create, name='visitor_create'),
    path('visitors/<int:pk>/edit/', views.visitor_edit, name='visitor_edit'),
]
