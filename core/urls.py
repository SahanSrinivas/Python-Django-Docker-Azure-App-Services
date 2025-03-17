# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.create_item, name='create_item'),
     path('', views.item_list, name='item_list'),
]
