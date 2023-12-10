from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.timezone import now, timedelta

from core.models import Contact
from .models import Event, Invitation


class InvitationModelTests(TestCase):
    def setUp(self):
        # Create necessary instances for ForeignKey fields
        self.contact = Contact.objects.create(
            name="John Doe", email="john@example.com"
        )
        self.event = Event.objects.create(
            name="Sample Event",
            start_time=now(),
            end_time=now() + timedelta(hours=1),
        )

    def test_num_guests_cannot_be_negative(self):
        invitation = Invitation(
            num_guests=3,
            invitee=self.contact,
            event=self.event,
            is_attending=True,
        )
        invitation.full_clean()
        with self.assertRaisesMessage(
            ValidationError, "Ensure this value is greater than or equal to 0."
        ):
            invitation.num_guests = -1
            invitation.full_clean()
