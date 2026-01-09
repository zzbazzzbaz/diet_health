from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.index, name='index'),
    path('start/', views.start, name='start'),
    path('question/<int:index>/', views.question, name='question'),
    path('submit/', views.submit, name='submit'),
    path('result/', views.result, name='result'),
]
