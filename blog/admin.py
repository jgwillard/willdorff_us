from django.contrib import admin
from django.db import models

from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget

from blog.models import Post


@admin.register(Post)
class PostAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }
