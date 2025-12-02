from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Count
from .models import Salon, Message, Track, Vote
from .forms import SalonForm, MessageForm
from .utils import search_jamendo_tracks
import random

@login_required
def salon_list(request):
    salons_communautaires = Salon.objects.filter(type='communautaire')
    salons_thematiques = Salon.objects.filter(type='thematique')
    return render(request, 'salons/salon_list.html', {
        'salons_communautaires': salons_communautaires,
        'salons_thematiques': salons_thematiques,
    })

@login_required
def salon_detail(request, salon_id):
    salon = get_object_or_404(Salon, id=salon_id)
    
    # Ajouter l'utilisateur comme membre s'il ne l'est pas déjà
    if request.user not in salon.membres.all():
        salon.membres.add(request.user)
    
    messages_list = salon.messages.all().order_by('-timestamp')[:50]

    # Obtenir les votes actuels
    votes = salon.votes.values('track').annotate(count=Count('track')).order_by('-count')[:5]
    voted_tracks = []
    for vote in votes:
        track = Track.objects.get(id=vote['track'])
        voted_tracks.append({'track': track, 'count': vote['count']})
    
    # Chercher des morceaux aléatoires depuis Jamendo pour proposer au vote
    suggested_tracks = search_jamendo_tracks(query='music', limit=5)
    
    form = MessageForm()

    salons_communautaires = Salon.objects.filter(type='communautaire')
    salons_thematiques = Salon.objects.filter(type='thematique')
    
    context = {
        'salons_communautaires': salons_communautaires,
        'salons_thematiques': salons_thematiques,
        'salon': salon,
        'messages': messages_list,
        'voted_tracks': voted_tracks,
        'suggested_tracks': suggested_tracks,
        'form': form,
    }
    return render(request, 'salons/salon_detail.html', context)

@login_required
@require_POST
def send_message(request, salon_id):
    salon = get_object_or_404(Salon, id=salon_id)
    form = MessageForm(request.POST)
    if form.is_valid():
        message = form.save(commit=False)
        message.salon = salon
        message.user = request.user
        message.save()
    
    # Retourner le fragment HTMX
    messages_list = salon.messages.all().order_by('timestamp')[:50]
    return render(request, 'salons/messages_partial.html', {
        'messages': messages_list,
        'salon': salon
    })

@login_required
def get_messages(request, salon_id):
    """Vue pour HTMX polling des messages"""
    salon = get_object_or_404(Salon, id=salon_id)
    messages_list = salon.messages.all().order_by('timestamp')[:50]
    return render(request, 'salons/messages_partial.html', {
        'messages': messages_list,
        'salon': salon
    })

@login_required
@require_POST
def vote_track(request, salon_id):
    salon = get_object_or_404(Salon, id=salon_id)
    track_id = request.POST.get('track_id')
    
    if track_id:
        track = get_object_or_404(Track, id=track_id)
        # Supprimer les anciens votes de l'utilisateur dans ce salon
        Vote.objects.filter(salon=salon, user=request.user).delete()
        # Créer le nouveau vote
        Vote.objects.create(salon=salon, user=request.user, track=track)
    
    # Retourner les votes mis à jour
    votes = salon.votes.values('track').annotate(count=Count('track')).order_by('-count')[:5]
    voted_tracks = []
    for vote in votes:
        track = Track.objects.get(id=vote['track'])
        voted_tracks.append({'track': track, 'count': vote['count']})
    
    return render(request, 'salons/votes_partial.html', {
        'voted_tracks': voted_tracks,
        'salon': salon
    })

@login_required
def create_salon(request):
    if request.method == 'POST':
        form = SalonForm(request.POST, request.FILES)
        if form.is_valid():
            salon = form.save(commit=False)
            salon.type = 'thematique'
            salon.owner = request.user
            salon.save()
            salon.membres.add(request.user)
            # messages.success(request, f'Salon "{salon.nom}" créé avec succès !')
            return redirect('salon_detail', salon_id=salon.id)
    else:
        form = SalonForm()

    salons_communautaires = Salon.objects.filter(type='communautaire')
    salons_thematiques = Salon.objects.filter(type='thematique')

    return render(request, 'salons/create_salon.html', {
        'salons_communautaires': salons_communautaires,
        'salons_thematiques': salons_thematiques,
        'form': form
    })

@login_required
def add_suggested_track(request, salon_id):
    """Ajouter une piste suggérée par Jamendo à la base"""
    jamendo_id = request.GET.get('jamendo_id')
    titre = request.GET.get('titre')
    artiste = request.GET.get('artiste')
    album = request.GET.get('album', '')
    cover_url = request.GET.get('cover_url', '')
    preview_url = request.GET.get('preview_url')
    duree = request.GET.get('duree', 30)
    
    track, created = Track.objects.get_or_create(
        jamendo_id=jamendo_id,
        defaults={
            'titre': titre,
            'artiste': artiste,
            'album': album,
            'cover_url': cover_url,
            'preview_url': preview_url,
            'duree': duree
        }
    )
    
    return JsonResponse({'track_id': track.id, 'created': created})