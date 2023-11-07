import os
import django
from django.core.management.base import BaseCommand
from django.utils import timezone

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "wildorff_us.settings"
)  # Change 'your_project_name' to your project's settings module
django.setup()

from events.models import Event, Invitee, Invitation


class Command(BaseCommand):
    help = "Initialize development environment"

    def handle(self, *args, **options):
        # Execute your script or command
        try:
            e = Event(
                name="Test", description="A test event", date=timezone.now()
            )
            e.save()
            i = Invitee(name="John", email="jgwil2@gmail.com")
            i.save()
            e.invitees.add(i)
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Command execution failed: {e}")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("Initialization completed successfully")
            )
