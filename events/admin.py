from django.conf import settings
from django.contrib import admin, messages
from django.core.mail import send_mail
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import path, reverse

from django_ckeditor_5.widgets import CKEditor5Widget

from core.models import ContactList

from .models import Event, Invitation


class InvitationInline(admin.TabularInline):
    model = Invitation
    extra = 1

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("invitee", "event")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                "invite-contacts-from-list/",
                self.invite_contacts_from_list,
                name="events_event_invite_contacts_from_list",
            )
        ]
        return new_urls + urls

    readonly_fields = ("total_expected_guests",)
    formfield_overrides = {
        models.TextField: {
            "widget": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="extends"
            )
        }
    }
    inlines = [InvitationInline]
    actions = [
        "email_invitations",
        "email_reminders",
        "invite_contacts_from_list",
    ]

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
                        request,
                        f"Invitation has already been sent to {invitation.invitee.email}. Invitation not re-sent.",
                    )

            messages.success(
                request, f"Successfully emailed invitations for {event}"
            )

    @admin.action(description="Email reminders for selected events")
    def email_reminders(self, request, queryset):
        for event in queryset:
            # NOTE see https://stackoverflow.com/questions/2005953/access-fields-in-django-intermediate-model
            for invitation in event.invitation_set.all():
                if invitation.is_sent:
                    try:
                        subject = f"Reminder: {event.name}"
                        template_name = "events/emails/reminder_email.html"
                        has_responded = invitation.is_attending is not None
                        link = settings.HOST + reverse(
                            "rsvp", kwargs={"unique_id": invitation.unique_id}
                        )
                        context = {
                            "subject": subject,
                            "event": event,
                            "invitation": invitation,
                            "link": link,
                            "has_responded": has_responded,
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
                    except Exception as e:
                        messages.error(
                            request,
                            f"Error occurred while trying to email invitation to {invitation.invitee.email}: {str(e)}",
                        )
                else:
                    messages.warning(
                        request,
                        f"{invitation.invitee.display_name} has not been sent an invitation. Reminder not sent.",
                    )

            messages.success(
                request, f"Successfully emailed reminders for {event}"
            )

    @admin.action(
        description="Invite all contacts on a contact list to selected events"
    )
    def invite_contacts_from_list(self, request, queryset=None):
        if "apply" in request.POST:
            contact_list_id = int(request.POST.get("contact_list"))
            contact_list = ContactList.objects.get(pk=contact_list_id)
            selected_ids = request.POST.getlist("selected_ids")
            queryset = Event.objects.filter(pk__in=selected_ids)
            for event in queryset:
                try:
                    for contact in contact_list.contacts.all():
                        Invitation.objects.create(event=event, invitee=contact)

                    messages.success(
                        request,
                        f"Successfully created invitations to {event} for {contact_list}",
                    )

                except Exception as e:
                    messages.error(
                        request,
                        f"Error ocurred when creating invitations to {event} for {contact_list}: {str(e)}",
                    )

            return HttpResponseRedirect(
                reverse("admin:events_event_changelist")
            )

        return render(
            request,
            "admin/invite_contacts.html",
            context={
                "events": queryset,
                "contact_lists": ContactList.objects.all(),
            },
        )


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    readonly_fields = ("unique_id",)
