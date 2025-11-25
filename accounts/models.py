from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """Utilisateur personnalisé"""
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.username

class Profile(models.Model):
    """Profil utilisateur"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True, max_length=500)
    date_naissance = models.DateField(blank=True, null=True)
    preferences_musicales = models.TextField(blank=True, help_text="Genres musicaux préférés")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profil de {self.user.username}"
    
    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profils"