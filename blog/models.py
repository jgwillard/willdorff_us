from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=200)
    is_published = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # set published date when publishing
        if self.is_published and not self.published_date:
            self.published_date = timezone.now()

        # unset published date when unpublishing
        if not self.is_published and self.published_date:
            self.published_date = None

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
