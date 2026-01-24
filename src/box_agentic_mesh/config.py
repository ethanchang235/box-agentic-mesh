"""
Configuration module for Box Agentic Mesh.

Loads environment variables for Box API authentication.
Supports refresh tokens for long-lived access without manual rotation.
"""

import os
from dotenv import load_dotenv
from boxsdk import Client, OAuth2

try:
    from boxsdk.auth.oauth2 import RefreshToken as OAuth2RefreshToken
except ImportError:
    RefreshToken = None  # Fallback for older Box SDK versions

# Load environment variables from .env file
load_dotenv()

# Box API credentials
# Obtain these from the Box Developer Console
# https://app.box.com/developers/console

BOX_CLIENT_ID = os.getenv("BOX_CLIENT_ID")
"""OAuth 2.0 Client ID for the Box application."""

BOX_CLIENT_SECRET = os.getenv("BOX_CLIENT_SECRET")
"""OAuth 2.0 Client Secret for the Box application."""

BOX_ACCESS_TOKEN = os.getenv("BOX_ACCESS_TOKEN")
"""OAuth 2.0 Access Token for API authentication.

For development, use a developer token from the Box Console.
For production, implement OAuth 2.0 flow to obtain tokens securely.
"""

BOX_REFRESH_TOKEN = os.getenv("BOX_REFRESH_TOKEN")
"""Optional: Refresh token for long-lived access (60 days instead of 60 minutes)."""


def get_box_client() -> Client:
    """Create and return an authenticated Box client.

    Automatically uses refresh token if available, falls back to access token.
    This enables long-lived access without manual token rotation.

    Returns:
        Authenticated Box SDK Client instance.

    Raises:
        ValueError: If no authentication credentials are configured.
    """
    # Try refresh token first for longer sessions
    if BOX_REFRESH_TOKEN and RefreshToken:
        try:
            oauth = OAuth2RefreshToken(
                client_id=BOX_CLIENT_ID,
                client_secret=BOX_CLIENT_SECRET,
                refresh_token=BOX_REFRESH_TOKEN,
            )
            token_info = oauth.refresh({})
            if "access_token" in token_info:
                # Store the new access token for future use
                with open(".env", "w") as f:
                    f.write(f"BOX_ACCESS_TOKEN={token_info['access_token']}\n")
                print("Refreshed access token for 60-day duration")
                # Use the new token
                oauth.access_token = token_info["access_token"]
            else:
                print("Refresh failed, falling back to access token")
        except Exception as e:
            print(f"Refresh failed: {e}")
            # Fall back to access token
            oauth = OAuth2(
                client_id=BOX_CLIENT_ID,
                client_secret=BOX_CLIENT_SECRET,
                access_token=BOX_ACCESS_TOKEN,
            )
    else:
        # Fall back to direct access token
        oauth = OAuth2(
            client_id=BOX_CLIENT_ID,
            client_secret=BOX_CLIENT_SECRET,
            access_token=BOX_ACCESS_TOKEN,
        )

    return Client(oauth)
