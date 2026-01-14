# Box API Setup Guide

Configure Box API credentials to authenticate with the Box Agentic Mesh.

## Prerequisites

1. Box Developer Account
2. Access to [Box Developer Console](https://app.box.com/developers/console)

## Setup Steps

### 1. Create a Box App

1. Navigate to [Box Developer Console](https://app.box.com/developers/console)
2. Click "Create New App"
3. Select "Custom App"
4. Choose authentication method:
   - **OAuth 2.0**: User-facing applications
   - **JWT (Server Authentication)**: Service-to-service integrations

### 2. Configure App Settings

- **App Name**: Box Agentic Mesh
- **Scopes**: Enable `root_readwrite` for full access
- **Redirect URIs**: `http://localhost:8000/callback` (if using OAuth flow)

### 3. Obtain Credentials

After app creation, note these values:
- **Client ID**: OAuth application identifier
- **Client Secret**: OAuth application secret
- **Access Token**: For quick testing (limited time)

For production, implement OAuth 2.0 flow to obtain tokens securely.

## Environment Configuration

Create a `.env` file in the project root:

```bash
BOX_CLIENT_ID=your_client_id
BOX_CLIENT_SECRET=your_client_secret
BOX_ACCESS_TOKEN=your_access_token
DEMO_FOLDER_ID=your_test_folder_id
```

The application loads these values automatically via `python-dotenv`.

## Quick Start

1. Set environment variables in `.env`
2. Run API server: `PYTHONPATH=src python -m uvicorn box_agentic_mesh.api:app --port 8000`
3. Access docs at: `http://localhost:8000/docs`

## Security Notes

- Never commit `.env` to version control
- Rotate access tokens regularly
- Use minimal required scopes for production deployments
