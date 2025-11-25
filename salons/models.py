from django.db import models
from django.conf import settings

class Salon(models.Model):
    """Salons de discussion musicaux"""
    TYPE_CHOICES = [
        ('communautaire', 'Communautaire'),
        ('thematique', 'Thématique'),
    ]
    
    nom = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='thematique')
    description = models.TextField()
    image = models.ImageField(upload_to='salons/', blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='salons_owned')
    membres = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='salons_joined', blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    current_track = models.ForeignKey('Track', on_delete=models.SET_NULL, null=True, blank=True, related_name='current_in_salon')
    
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = "Salon"
        verbose_name_plural = "Salons"
        ordering = ['-date_creation']

class Track(models.Model):
    """Piste musicale (Jamendo)"""
    titre = models.CharField(max_length=200)
    artiste = models.CharField(max_length=200)
    album = models.CharField(max_length=200, blank=True)
    cover_url = models.URLField(max_length=500, blank=True)
    preview_url = models.URLField(max_length=500)
    jamendo_id = models.CharField(max_length=100, unique=True)
    duree = models.IntegerField(help_text="Durée en secondes")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.titre} - {self.artiste}"
    
    class Meta:
        verbose_name = "Piste"
        verbose_name_plural = "Pistes"

class Message(models.Model):
    """Messages dans les salons"""
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contenu = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} dans {self.salon.nom}"
    
    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['timestamp']

class Vote(models.Model):
    """Votes pour les morceaux suivants"""
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Vote de {self.user.username} pour {self.track.titre}"
    
    class Meta:
        verbose_name = "Vote"
        verbose_name_plural = "Votes"
        unique_together = ['salon', 'user', 'track']
        ordering = ['-timestamp']