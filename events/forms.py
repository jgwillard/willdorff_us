from django.forms import ModelForm

from .models import Invitation


class InvitationForm(ModelForm):
    class Meta:
        model = Invitation
        fields = ["is_confirmed", "num_guests"]
