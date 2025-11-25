from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notification
from django.utils import timezone

@login_required
def notification_list(request):
    """Liste des notifications actives"""
    notifications = Notification.objects.filter(
        visible=True,
        date_publication__lte=timezone.now()
    ).filter(
        date_expiration__isnull=True
    ) | Notification.objects.filter(
        visible=True,
        date_publication__lte=timezone.now(),
        date_expiration__gte=timezone.now()
    )
    
    return render(request, 'notifications/notification_list.html', {
        'notifications': notifications.order_by('-date_publication')
    })

@login_required
def check_notifications(request):
    """API pour vérifier s'il y a de nouvelles notifications (pour Alpine.js)"""
    has_recent = Notification.objects.filter(
        visible=True,
        date_publication__lte=timezone.now(),
        date_publication__gte=timezone.now() - timezone.timedelta(minutes=1)
    ).exists()
    
    return JsonResponse({'has_recent': has_recent})