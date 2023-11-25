from django.conf import settings
from django.contrib import admin, messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse

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
                if not invitation.is_sent:
                    try:
                        subject = f"RSVP to {event.name}"
                        template_name = "events/emails/rsvp_email.html"
                        link = settings.HOST + reverse(
                            "rsvp", kwargs={"unique_id": invitation.unique_id}
                        )
                        context = {
                            "subject": subject,
                            "event": event,
                            "invitation": invitation,
                            "link": link,
                        }

                        html_message = render_to_string(template_name, context)
                        recipient_list = [invitation.invitee.email]
                        send_mail(
                            subject,
                            "",
                            settings.DEFAULT_FROM_EMAIL,
                            recipient_list,
                            html_message=html_message,
                            fail_silently=False,
                        )
                        invitation.is_sent = True
                        invitation.save()
                    except Exception as e:
                        messages.error(
                            request,
                            f"Error occurred while trying to email invitation to {invitation.invitee.email}: {str(e)}",
                        )
                else:
                    messages.warning(
                        request, "Some invitations have already been sent"
                    )

            messages.success(
                request, f"Successfully emailed invitations for {event}"
            )


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    readonly_fields = ("unique_id",)
