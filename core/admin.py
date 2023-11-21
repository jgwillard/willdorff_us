from django.contrib import admin

from .models import Contact

admin.site.site_header = "willdorff.us administration"


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass
