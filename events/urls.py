from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('calendar/', views.event_calendar, name='event_calendar'),
    path('create/', views.event_create, name='event_create'),
    path('<int:pk>/', views.event_detail, name='event_detail'),
    path('<int:pk>/register/', views.event_register, name='event_register'),
]
