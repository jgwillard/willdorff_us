from django.db import models


class Invitee(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    date = models.DateTimeField()
    invitees = models.ManyToManyField(Invitee, through="Invitation")

    def __str__(self) -> str:
        return f"{self.name} {self.date.date()}"


class Invitation(models.Model):
    invitee = models.ForeignKey(Invitee, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)
    num_guests = models.IntegerField("number of extra guests", default=0)

    def __str__(self) -> str:
        return f"{self.invitee}::{self.event}"
