from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .forms import InvitationForm
from .models import Invitation


class InvitationDetailView(generic.DetailView):
    model = Invitation
    template_name = "events/rsvp.html"
    slug_field = "unique_id"
    slug_url_kwarg = "unique_id"
    context_object_name = "invitation"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = InvitationForm(instance=self.object)
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = InvitationForm(request.POST, instance=self.object)
        if form.is_valid():
            form.save()
            # record that a response has been given
            self.object.has_responded = True
            self.object.save()
            return HttpResponseRedirect(
                reverse(
                    "rsvp_thanks", kwargs={"unique_id": self.object.unique_id}
                )
            )
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class InvitationConfirmationlView(generic.DetailView):
    model = Invitation
    template_name = "events/rsvp_thanks.html"
    slug_field = "unique_id"
    slug_url_kwarg = "unique_id"
