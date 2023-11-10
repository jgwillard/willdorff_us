from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic

from .forms import InvitationForm
from .models import Invitation


class InvitationDetailView(generic.DetailView):
    template_name = "events/rsvp.html"

    def get_object(self, unique_id):
        return get_object_or_404(Invitation, unique_id=unique_id)

    def get(self, request, unique_id):
        invitation = self.get_object(unique_id)
        form = InvitationForm(instance=invitation)
        return render(
            request,
            self.template_name,
            {"form": form, "invitation": invitation},
        )

    def post(self, request, unique_id):
        invitation = self.get_object(unique_id)
        form = InvitationForm(request.POST, instance=invitation)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                "/success-url/"
            )  # Replace with your success URL
        return render(
            request,
            self.template_name,
            {"form": form, "invitation": invitation},
        )
