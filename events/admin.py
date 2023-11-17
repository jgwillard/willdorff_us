from django.contrib import admin

from .models import Event, Invitation


class InvitationInline(admin.TabularInline):
    model = Invitation
    extra = 1


class EventAdmin(admin.ModelAdmin):
    inlines = [InvitationInline]


class InvitationAdmin(admin.ModelAdmin):
    readonly_fields = ("unique_id",)


admin.site.register(Event, EventAdmin)
admin.site.register(Invitation, InvitationAdmin)
