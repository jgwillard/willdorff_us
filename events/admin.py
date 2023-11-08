from django.contrib import admin

from .models import Event, Invitation


class InvitationAdmin(admin.ModelAdmin):
    readonly_fields = ("unique_id",)


admin.site.register(Event)
admin.site.register(Invitation, InvitationAdmin)
