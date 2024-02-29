from django.contrib import admin
from django.db import models

from unfold.admin import ModelAdmin
from django_ckeditor_5.widgets import CKEditor5Widget

from blog.models import Post


@admin.register(Post)
class PostAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {
            "widget": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="extends"
            ),
        }
    }
