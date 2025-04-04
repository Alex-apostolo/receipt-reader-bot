from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os
import json
from typing import Optional
from app.config import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_REDIRECT_URI,
)
from app.services.firestore_service import FirestoreService


class GoogleService:
    # If modifying these scopes, delete the file token.json.
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
    ]

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
        # self.spreadsheet_id = SPREADSHEET_ID
        self.sheets_service = None
        self.firestore_service = FirestoreService()

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
        """Save credentials to Firestore."""
        self.firestore_service.save_user_credentials(user_id, credentials)

    def load_credentials(self, user_id: str) -> Optional[Credentials]:
        """Load credentials from Firestore."""
        creds_data = self.firestore_service.get_user_credentials(user_id)
        if not creds_data:
            return None

        return Credentials(
            token=creds_data["token"],
            refresh_token=creds_data["refresh_token"],
            token_uri=creds_data["token_uri"],
            client_id=creds_data["client_id"],
            client_secret=creds_data["client_secret"],
            scopes=creds_data["scopes"],
        )

    def is_authenticated(self, user_id: str) -> bool:
        """Check if user is authenticated."""
        return self.load_credentials(user_id) is not None

    def revoke_credentials(self, user_id: str):
        """Revoke user's credentials."""
        self.firestore_service.delete_user_data(user_id)
