from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .forms import InvitationForm
from .models import Invitation


class InvitationDetailView(generic.DetailView):
    model = Invitation
    template_name = "events/rsvp.html"
    slug_field = "unique_id"
    slug_url_kwarg = "unique_id"
    context_object_name = "invitation"

    def get_queryset(self):
        return super().get_queryset().select_related("invitee", "event")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        now = timezone.now()
        if self.object.event.end_time < now:
            raise Http404("Event is in the past")
        form = InvitationForm(instance=self.object)
        has_visited = self.object.is_attending is not None
        context = self.get_context_data(form=form, has_visited=has_visited)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = InvitationForm(request.POST, instance=self.object)
        if form.is_valid():
            form.save()
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
