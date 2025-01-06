from django.urls import path
from . import views

urlpatterns = [
    path('', views.tweet_list, name='tweet_list'),
    path('<slug:slug>/', views.tweet_detail, name='tweet_detail'),
]
