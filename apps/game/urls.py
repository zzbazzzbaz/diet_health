from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.index, name='index'),
    path('crowd/', views.select_crowd, name='crowd'),
    path('meal/', views.select_meal, name='meal'),
    path('food/', views.select_food, name='food'),
    path('api/foods/', views.get_foods, name='foods_api'),
    path('evaluate/', views.evaluate, name='evaluate'),
    path('result/', views.result, name='result'),
]
