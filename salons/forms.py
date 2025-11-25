from django import forms
from .models import Salon, Message

class SalonForm(forms.ModelForm):
    class Meta:
        model = Salon
        fields = ['nom', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['contenu']
        widgets = {
            'contenu': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Votre message...'}),
        }