from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=200)
    given_name = models.CharField(max_length=200)
    family_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"
