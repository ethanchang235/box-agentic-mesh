"""
Configuration module for Box Agentic Mesh.

Loads environment variables for Box API authentication.
Ensure these variables are set in a .env file or environment before use.
"""

import os
from dotenv import load_dotenv

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

BOX_ENTERPRISE_ID = os.getenv("BOX_ENTERPRISE_ID")
"""Enterprise ID for JWT authentication (optional)."""
