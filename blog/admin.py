from django.contrib import admin
from django.db import models

from django_ckeditor_5.widgets import CKEditor5Widget

from blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ["author", "published_date", "created_date"]
    formfield_overrides = {
        models.TextField: {
            "widget": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="extends"
            ),
        }
    }

    def save_form(self, request, form, change):
        obj = super().save_form(request, form, change)
        obj.author = request.user if request.user.is_authenticated else None
        return obj
