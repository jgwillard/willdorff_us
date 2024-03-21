from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum, F, Case, When, Value
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
        return (
            self.invitation_set.filter(is_attending=True).aggregate(
                total_guests=Sum(
                    Case(
                        When(is_attending=True, then=F("num_guests") + 1),
                        default=Value(0),
                        output_field=models.IntegerField(),
                    )
                )
            )["total_guests"]
            or 0
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
