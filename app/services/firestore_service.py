import firebase_admin
from firebase_admin import credentials, firestore
from typing import Optional, Dict, Any
from google.oauth2.credentials import Credentials


class FirestoreService:
    def __init__(self):
        # Initialize Firebase Admin SDK if not already initialized
        if not firebase_admin._apps:
            cred = credentials.Certificate(
                "receipt-reader-bot-firebase-adminsdk-fbsvc-77091402e7.json"
            )
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def save_user_credentials(self, user_id: str, credentials: Credentials):
        """Save user's Google credentials to Firestore."""
        creds_data = {
            "token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": credentials.scopes,
        }

        self.db.collection("users").document(user_id).set(
            {
                "google_credentials": creds_data,
                "updated_at": firestore.SERVER_TIMESTAMP,
            },
            merge=True,
        )

    def get_user_credentials(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user's Google credentials from Firestore."""
        doc = self.db.collection("users").document(user_id).get()
        if doc.exists:
            return doc.to_dict().get("google_credentials")
        return None

    def save_spreadsheet_id(self, user_id: str, spreadsheet_id: str):
        """Save user's spreadsheet ID to Firestore."""
        self.db.collection("users").document(user_id).set(
            {
                "spreadsheet_id": spreadsheet_id,
                "updated_at": firestore.SERVER_TIMESTAMP,
            },
            merge=True,
        )

    def get_spreadsheet_id(self, user_id: str) -> Optional[str]:
        """Get user's spreadsheet ID from Firestore."""
        doc = self.db.collection("users").document(user_id).get()
        if doc.exists:
            return doc.to_dict().get("spreadsheet_id")
        return None

    def delete_user_data(self, user_id: str):
        """Delete all user data from Firestore."""
        self.db.collection("users").document(user_id).delete()
