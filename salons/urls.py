from django.urls import path
from . import views

urlpatterns = [
    path('', views.salon_list, name='salon_list'),
    path('<int:salon_id>/', views.salon_detail, name='salon_detail'),
    path('<int:salon_id>/send/', views.send_message, name='send_message'),
    path('<int:salon_id>/messages/', views.get_messages, name='get_messages'),
    path('<int:salon_id>/vote/', views.vote_track, name='vote_track'),
    path('<int:salon_id>/add-track/', views.add_suggested_track, name='add_suggested_track'),
    path('create/', views.create_salon, name='create_salon'),
]