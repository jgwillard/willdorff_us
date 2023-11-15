from django.db import models
import uuid

from core.models import Contact


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    date = models.DateTimeField()
    invitees = models.ManyToManyField(Contact, through="Invitation")

    def __str__(self) -> str:
        return f"{self.name} {self.date.date()}"


class Invitation(models.Model):
    unique_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True
    )
    invitee = models.ForeignKey(Contact, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    has_responded = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    num_guests = models.IntegerField("number of extra guests", default=0)

    def __str__(self) -> str:
        return f"{self.invitee}::{self.event}"
