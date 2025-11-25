from django.shortcuts import render

def home(request):
    """Page d'accueil"""
    return render(request, 'core/home.html')

def about(request):
    """Page À propos"""
    return render(request, 'core/about.html')

def contact(request):
    """Page Contact"""
    return render(request, 'core/contact.html')