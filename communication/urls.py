from django.urls import path
from . import views

urlpatterns = [
    path('announcements/', views.announcement_list, name='announcement_list'),
    path('announcements/create/', views.announcement_create, name='announcement_create'),
    path('inbox/', views.inbox, name='inbox'),
    path('send/', views.send_message, name='send_message'),
    path('messages/<int:pk>/', views.message_detail, name='message_detail'),
]
