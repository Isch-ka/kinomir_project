from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    # Добавляем путь для групп с slug-параметром
    path('group/<slug:slug>/', views.group_posts),
]