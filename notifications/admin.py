from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['titre', 'date_publication', 'date_expiration', 'visible', 'est_active']
    list_filter = ['visible', 'date_publication']
    search_fields = ['titre', 'contenu']
    
    def est_active(self, obj):
        return obj.est_active()
    est_active.boolean = True
    est_active.short_description = 'Active'