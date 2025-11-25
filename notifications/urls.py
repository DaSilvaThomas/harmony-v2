from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('check/', views.check_notifications, name='check_notifications'),
]