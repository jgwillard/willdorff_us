import os
import subprocess

import django
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "willdorff_us.settings")
django.setup()

from core.models import Contact
from events.models import Event


class Command(BaseCommand):
    help = "Initialize development environment"

    def handle(self, *args, **options):
        try:
            subprocess.run(["rm", "-f", "db.sqlite3"], check=True)
        except subprocess.CalledProcessError as e:
            self.stdout.write(
                self.style.ERROR(f"Command execution failed: {e}")
            )
        else:
            self.stdout.write(self.style.SUCCESS("Database deleted"))

        try:
            output = call_command(
                "makemigrations", stdout=self.stdout, stderr=self.stderr
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Command execution failed: {e}")
            )
        else:
            self.stdout.write(self.style.SUCCESS(output))

        try:
            output = call_command(
                "migrate", stdout=self.stdout, stderr=self.stderr
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Command execution failed: {e}")
            )
        else:
            self.stdout.write(self.style.SUCCESS(output))

        try:
            username = "herb"
            email = "herb@example.com"
            password = "hellomuriel!"

            output = call_command(
                "createsuperuser",
                interactive=False,
                username=username,
                email=email,
                stdout=self.stdout,
                stderr=self.stderr,
            )

            from django.contrib.auth.models import User

            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Command execution failed: {e}")
            )
        else:
            self.stdout.write(self.style.SUCCESS(output))

        try:
            e = Event(
                name="Test", description="A test event", date=timezone.now()
            )
            e.save()
            c = Contact(name="John", email="jgwil2@gmail.com")
            c.save()
            e.invitees.add(c)
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Command execution failed: {e}")
            )
        else:
            self.stdout.write(self.style.SUCCESS("Data created"))
