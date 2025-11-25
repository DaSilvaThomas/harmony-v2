from django.core.management.base import BaseCommand
from django.utils import timezone
from notifications.models import Notification

class Command(BaseCommand):
    help = 'Publie les notifications programmées'

    def handle(self, *args, **options):
        now = timezone.now()
        notifications = Notification.objects.filter(
            visible=True,
            date_publication__lte=now
        )
        
        count = notifications.count()
        self.stdout.write(
            self.style.SUCCESS(f'{count} notification(s) active(s)')
        )