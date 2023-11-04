from django.db import models


class Guest(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    date = models.DateTimeField()
    guests = models.ManyToManyField(Guest)

    def __str__(self) -> str:
        return f"{self.name} {self.date}"
