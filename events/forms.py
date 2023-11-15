from django.forms import ModelForm

from .models import Invitation


class InvitationForm(ModelForm):
    class Meta:
        model = Invitation
        fields = ["is_confirmed", "num_guests"]
        labels = {
            "is_confirmed": "Will you be attending?",
            "num_guests": "How many people are you bringing with you?",
        }
