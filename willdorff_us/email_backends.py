import base64
from email.mime.text import MIMEText

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from core.models import GoogleOAuthToken


SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def _build_credentials(token_obj: GoogleOAuthToken) -> Credentials:
    """
    Rehydrate Credentials from DB and ensure a valid access token.
    """
    data = token_obj.token_json

    creds = Credentials(
        token=data.get("token"),
        refresh_token=data.get("refresh_token"),
        token_uri=data.get("token_uri"),
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        scopes=SCOPES,
    )

    # Refresh if needed and persist updated access token
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            token_obj.token_json = {
                **token_obj.token_json,
                "token": creds.token,
            }
            token_obj.save(update_fields=["token_json"])
        else:
            raise RuntimeError("Gmail credentials are invalid and cannot be refreshed.")

    return creds


def _gmail_service(creds: Credentials):
    return build("gmail", "v1", credentials=creds, cache_discovery=False)


class GmailAPIBackend(BaseEmailBackend):
    """
    Drop-in replacement for Django's email backend using Gmail API.
    """

    def send_messages(self, email_messages):
        if not email_messages:
            return 0

        token_obj = GoogleOAuthToken.objects.get(name="default")
        creds = _build_credentials(token_obj)
        service = _gmail_service(creds)

        sent_count = 0

        for message in email_messages:
            mime = message.message()

            raw = base64.urlsafe_b64encode(mime.as_bytes()).decode()

            service.users().messages().send(
                userId="me",
                body={"raw": raw},
            ).execute()

            sent_count += 1

        return sent_count
