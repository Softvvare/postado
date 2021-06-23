from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('register/', views.register, name='register'),
    path('create/', views.create, name='create'),
    path('delete/<uuid:id>/', views.delete, name='delete'),
    path('like/<uuid:id>/', views.like, name='like'),
    path('<uuid:id>/comments', views.comments, name='comments'),
    path('profile/<str:user_name>', views.profile, name='profile'),
    path('follow/<str:user_name>', views.follow, name='follow'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('explore/', views.explore, name='explore'),
]
