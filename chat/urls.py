from django.urls import path
from . import views

urlpatterns = [
    path('messages/', views.navigator, name='navigator'),
    path('room/<str:name>/', views.room, name='room'),
]
