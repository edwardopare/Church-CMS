from django.urls import path
from . import views

urlpatterns = [
    path('', views.ministry_list, name='ministry_list'),
    path('create/', views.ministry_create, name='ministry_create'),
    path('<int:pk>/', views.ministry_detail, name='ministry_detail'),
    path('<int:pk>/edit/', views.ministry_edit, name='ministry_edit'),
    path('<int:pk>/add-member/', views.add_ministry_member, name='add_ministry_member'),
]
