from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from google_auth_oauthlib.flow import Flow

from .models import GoogleOAuthToken


SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def start_oauth(request):
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=SCOPES,
    )

    flow.redirect_uri = request.build_absolute_uri(
        reverse("admin:google_oauth_callback")
    )

    authorization_url, state = flow.authorization_url(
        access_type="offline",  # REQUIRED for refresh token
        prompt="consent",  # forces refresh token issuance
        include_granted_scopes="true",
    )

    request.session["oauth_state"] = state
    request.session["oauth_code_verifier"] = flow.code_verifier

    return redirect(authorization_url)


def oauth_callback(request):
    state = request.session.get("oauth_state")
    code_verifier = request.session.get("oauth_code_verifier")

    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=SCOPES,
        state=state,
    )

    flow.redirect_uri = request.build_absolute_uri(
        reverse("admin:google_oauth_callback")
    )
    flow.code_verifier = code_verifier  # restore PKCE verifier

    flow.fetch_token(authorization_response=request.build_absolute_uri())

    creds = flow.credentials

    # Save/update token
    GoogleOAuthToken.objects.update_or_create(
        name="default",
        defaults={
            "token_json": {
                "token": creds.token,
                "refresh_token": creds.refresh_token,
                "token_uri": creds.token_uri,
            }
        },
    )

    return HttpResponse("Authorization complete. You can close this window.")
