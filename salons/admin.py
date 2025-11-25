from django.contrib import admin
from .models import Salon, Track, Message, Vote

@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = ['nom', 'type', 'owner', 'date_creation']
    list_filter = ['type', 'date_creation']
    search_fields = ['nom', 'description']
    filter_horizontal = ['membres']

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ['titre', 'artiste', 'album', 'duree', 'jamendo_id']
    search_fields = ['titre', 'artiste', 'album']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'salon', 'timestamp', 'contenu']
    list_filter = ['salon', 'timestamp']
    search_fields = ['contenu', 'user__username']

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'salon', 'track', 'timestamp']
    list_filter = ['salon', 'timestamp']