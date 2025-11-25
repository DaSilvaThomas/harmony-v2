from django.db import models
from django.utils import timezone

class Notification(models.Model):
    """Notifications système"""
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    date_publication = models.DateTimeField()
    date_expiration = models.DateTimeField(blank=True, null=True)
    visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def est_active(self):
        """Vérifie si la notification est active"""
        now = timezone.now()
        if not self.visible:
            return False
        if self.date_publication > now:
            return False
        if self.date_expiration and self.date_expiration < now:
            return False
        return True
    
    def est_recente(self):
        """Vérifie si la notification a été publiée il y a moins d'une minute"""
        if not self.est_active():
            return False
        now = timezone.now()
        delta = now - self.date_publication
        return delta.total_seconds() < 60
    
    def __str__(self):
        return self.titre
    
    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-date_publication']