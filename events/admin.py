from django.contrib import admin

from .models import Event, Invitation, Invitee

admin.site.register(Event)
admin.site.register(Invitation)
admin.site.register(Invitee)
