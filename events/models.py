from django.core.validators import MinValueValidator
from django.db import models
import uuid

from core.models import Contact


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    invitees = models.ManyToManyField(Contact, through="Invitation")

    @property
    def total_expected_guests(self) -> int:
        return sum(
            map(
                lambda i: i.num_guests + 1 if i.is_attending else 0,
                self.invitation_set.all(),
            )
        )

    def __str__(self) -> str:
        return f"{self.name} {self.start_time.date()}"


class Invitation(models.Model):
    unique_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True
    )
    invitee = models.ForeignKey(Contact, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    is_sent = models.BooleanField(default=False)
    is_attending = models.BooleanField(default=None, null=True)
    num_guests = models.IntegerField(
        "number of extra guests", default=0, validators=[MinValueValidator(0)]
    )

    def __str__(self) -> str:
        return f"{self.invitee}::{self.event}"
