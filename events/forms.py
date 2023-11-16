from django.forms import BooleanField, ModelForm, RadioSelect

from .models import Invitation


class InvitationForm(ModelForm):
    class Meta:
        model = Invitation
        fields = ["is_attending", "num_guests"]
        labels = {
            "num_guests": "How many people are you bringing with you?",
        }

    is_attending = BooleanField(
        widget=RadioSelect(choices=((True, "Yes"), (False, "No"))),
        label="Will you be attending?",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(InvitationForm, self).__init__(*args, **kwargs)
        self.initial["is_attending"] = True
