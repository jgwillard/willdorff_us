from django.urls import path

from . import views

urlpatterns = [
    path("rsvp/<str:invitation_uuid>/", views.rsvp, name="rsvp"),
]
