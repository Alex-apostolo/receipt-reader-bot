from .base_handler import BaseHandler


class OAuthHandler(BaseHandler):
    async def handle_callback(self, code: str, state: str) -> bool:
        """Handle the OAuth callback with the authorization code."""
        try:
            credentials = self.google_auth.get_credentials_from_code(code)
            self.google_auth.save_credentials(credentials, state)
            # Send success message to user
            await self.bot.send_message(
                chat_id=state,
                text="Successfully authenticated with Google! ✅\n"
                "Now you can send me photos of your receipts, and I'll save them to your Google Sheet.",
            )
            return True
        except Exception as e:
            print(f"OAuth callback error: {str(e)}")
            # Send error message to user
            await self.bot.send_message(
                chat_id=state,
                text="❌ Authentication failed. Please try connecting your Google account again.",
            )
            return False
