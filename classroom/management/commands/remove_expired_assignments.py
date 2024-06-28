from django.core.management.base import BaseCommand
from datetime import datetime
from django.utils import timezone
from classroom.models import ClassAssignment

class Command(BaseCommand):
    help = 'Remove expired assignments'

    def handle(self, *args, **options):
        current_time = timezone.now()
        expired_assignments = ClassAssignment.objects.filter(end_time__lt=current_time)
        expired_assignments.delete()
        self.stdout.write(self.style.SUCCESS('Expired assignments removed successfully'))
