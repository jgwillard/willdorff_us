from django.contrib import admin

from .models import Event, Invitation


class InvitationInline(admin.TabularInline):
    model = Invitation
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [InvitationInline]


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    readonly_fields = ("unique_id",)
