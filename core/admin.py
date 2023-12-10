import csv
from io import TextIOWrapper
from django import forms
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path, reverse

from .models import Contact

admin.site.site_header = "willdorff.us administration"


class UploadFileForm(forms.Form):
    contacts_csv = forms.FileField()


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path("upload-csv/", self.upload_csv, name="upload_csv")]
        return new_urls + urls

    def upload_csv(self, request):
        user_url = reverse("admin:core_contact_changelist")
        if request.method == "POST":
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                with TextIOWrapper(request.FILES["contacts_csv"]) as csv_file:
                    try:
                        contacts_reader = csv.DictReader(csv_file)
                        failed_to_save_contacts = []
                        for row in contacts_reader:
                            name = row["Name"]
                            given_name = row["Given Name"]
                            family_name = row["Family Name"]
                            email = row["E-mail 1 - Value"]
                            try:
                                c = Contact(
                                    name=name,
                                    given_name=given_name,
                                    family_name=family_name,
                                    email=email,
                                )
                                c.full_clean()
                                c.save()
                            except Exception as e:
                                failed_to_save_contacts.append(
                                    f"{name}::{email} -- {e}"
                                )
                        if failed_to_save_contacts:
                            messages.warning(
                                request,
                                f"Failed to save the following contacts: {'; '.join(failed_to_save_contacts)}",
                            )
                        else:
                            messages.success(
                                request, "Contacts succesfully added"
                            )
                        return HttpResponseRedirect(user_url)
                    except Exception as e:
                        messages.error(
                            request,
                            f"Error ocurred when uploading file {csv_file.name}: {str(e)}",
                        )
                        return HttpResponseRedirect(user_url)
            else:
                messages.error(request, f"Form not valid: {str(form.errors)}")
                return HttpResponseRedirect(user_url)

        return HttpResponseRedirect(user_url)
