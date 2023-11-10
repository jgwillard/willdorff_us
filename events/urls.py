from django.urls import path

from .views import InvitationDetailView

urlpatterns = [
    path("rsvp/<uuid:unique_id>/", InvitationDetailView.as_view(), name="rsvp"),
]
