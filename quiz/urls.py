from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_home, name='quiz_home'),
    path('theme/<int:theme_id>/', views.quiz_theme, name='quiz_theme'),
    path('play/', views.quiz_play, name='quiz_play_random'),
    path('play/<int:theme_id>/', views.quiz_play, name='quiz_play'),
    path('result/', views.quiz_result, name='quiz_result'),
]