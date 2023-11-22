from django.contrib import admin

from .models import Event, Invitation


class InvitationInline(admin.TabularInline):
    model = Invitation
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [InvitationInline]
    actions = ["email_invitations"]

    @admin.action(description="Email invitations for selected events")
    def email_invitations(self, request, queryset):
        for event in queryset:
            # NOTE see https://stackoverflow.com/questions/2005953/access-fields-in-django-intermediate-model
            for invitation in event.invitation_set.all():
                # TODO send email
                print(invitation)


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    readonly_fields = ("unique_id",)
