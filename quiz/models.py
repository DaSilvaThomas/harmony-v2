from django.db import models
from django.conf import settings
import json

class QuizTheme(models.Model):
    """Thèmes de quiz"""
    nom = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='quiz/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = "Thème de Quiz"
        verbose_name_plural = "Thèmes de Quiz"

class Question(models.Model):
    """Questions de quiz"""
    TYPE_CHOICES = [
        ('texte', 'Texte'),
        ('audio', 'Audio'),
    ]
    
    theme = models.ForeignKey(QuizTheme, on_delete=models.CASCADE, related_name='questions')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='texte')
    question = models.TextField()
    audio_file = models.FileField(upload_to='quiz/audio/', blank=True, null=True)
    bonne_reponse = models.CharField(max_length=200)
    mauvaises_reponses = models.TextField(help_text="Liste JSON des mauvaises réponses")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_mauvaises_reponses(self):
        """Retourne la liste des mauvaises réponses"""
        try:
            return json.loads(self.mauvaises_reponses)
        except:
            return []
    
    def set_mauvaises_reponses(self, reponses_list):
        """Définit la liste des mauvaises réponses"""
        self.mauvaises_reponses = json.dumps(reponses_list)
    
    def get_all_reponses_shuffled(self):
        """Retourne toutes les réponses mélangées"""
        import random
        reponses = [self.bonne_reponse] + self.get_mauvaises_reponses()
        random.shuffle(reponses)
        return reponses
    
    def __str__(self):
        return f"{self.theme.nom} - {self.question[:50]}"
    
    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

class Score(models.Model):
    """Scores des utilisateurs"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='scores')
    theme = models.ForeignKey(QuizTheme, on_delete=models.CASCADE, related_name='scores')
    points_total = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.theme.nom}: {self.points_total} pts"
    
    class Meta:
        verbose_name = "Score"
        verbose_name_plural = "Scores"
        ordering = ['-points_total', '-date']