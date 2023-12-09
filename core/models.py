from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=200)
    given_name = models.CharField(max_length=200, blank=True)
    family_name = models.CharField(max_length=200, blank=True)
    email = models.CharField(max_length=200, unique=True, blank=False)

    @property
    def display_name(self):
        return self.given_name if self.given_name else self.name

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"
