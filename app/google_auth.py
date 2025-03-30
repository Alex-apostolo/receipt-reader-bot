from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os
import json
from typing import Optional
from .config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI


class GoogleAuth:
    # If modifying these scopes, delete the file token.json.
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

    def __init__(self):
        self.client_config = {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [GOOGLE_REDIRECT_URI],
                "scopes": self.SCOPES,
            }
        }
        self.redirect_uri = GOOGLE_REDIRECT_URI
        self.flow = Flow.from_client_config(self.client_config, self.SCOPES)
        self.flow.redirect_uri = self.redirect_uri

    def get_authorization_url(self, state: str = None) -> str:
        """Generate the authorization URL for Google OAuth."""
        auth_url, _ = self.flow.authorization_url(
            access_type="offline", include_granted_scopes="true", state=state
        )
        return auth_url

    def get_credentials_from_code(self, code: str) -> Credentials:
        """Exchange authorization code for credentials."""
        self.flow.fetch_token(code=code)
        return self.flow.credentials

    def save_credentials(self, credentials: Credentials, user_id: str):
        """Save credentials to a file."""
        creds_dir = "user_credentials"
        os.makedirs(creds_dir, exist_ok=True)

        creds_data = {
            "token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": credentials.scopes,
        }

        with open(
            os.path.join(creds_dir, f"{user_id}_google_creds.json"), "w"
        ) as token:
            json.dump(creds_data, token)

    def load_credentials(self, user_id: str) -> Optional[Credentials]:
        """Load credentials from file."""
        creds_path = os.path.join("user_credentials", f"{user_id}_google_creds.json")
        if not os.path.exists(creds_path):
            return None

        with open(creds_path) as token:
            creds_data = json.load(token)

        credentials = Credentials(
            token=creds_data["token"],
            refresh_token=creds_data["refresh_token"],
            token_uri=creds_data["token_uri"],
            client_id=creds_data["client_id"],
            client_secret=creds_data["client_secret"],
            scopes=creds_data["scopes"],
        )

        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
            self.save_credentials(credentials, user_id)

        return credentials

    def is_authenticated(self, user_id: str) -> bool:
        """Check if a user is authenticated with Google."""
        return self.load_credentials(user_id) is not None
