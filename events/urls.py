from django.urls import path

from .views import InvitationConfirmationlView, InvitationDetailView

urlpatterns = [
    path("rsvp/<uuid:unique_id>/", InvitationDetailView.as_view(), name="rsvp"),
    path(
        "rsvp/<uuid:unique_id>/thanks/",
        InvitationConfirmationlView.as_view(),
        name="rsvp_thanks",
    ),
]
