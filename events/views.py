from django.shortcuts import get_object_or_404, render

from .models import Invitation


def rsvp(request, invitation_uuid):
    invitation = get_object_or_404(Invitation, unique_id=invitation_uuid)
    return render(request, "events/rsvp.html", {"invitation": invitation})
