from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('register/', views.register, name='register'),
    path('create/', views.create, name='create'),
    path('delete/<uuid:id>/', views.delete, name='delete'),
]
