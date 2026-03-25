import os
import requests
from urllib.parse import urlencode

STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID", "")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET", "")
STRAVA_REDIRECT_URI = os.getenv("STRAVA_REDIRECT_URI", "http://localhost:8000/api/auth/strava/callback")

STRAVA_AUTH_URL = "https://www.strava.com/oauth/authorize"
STRAVA_TOKEN_URL = "https://www.strava.com/oauth/token"
STRAVA_API_BASE = "https://www.strava.com/api/v3"

def get_authorization_url():
    """Generate Strava OAuth authorization URL"""
    if not STRAVA_CLIENT_ID:
        return "http://localhost:5173?error=missing_client_id"

    params = {
        "client_id": STRAVA_CLIENT_ID,
        "redirect_uri": STRAVA_REDIRECT_URI,
        "response_type": "code",
        "scope": "read,activity:read_all,profile:read_all",
    }
    return f"{STRAVA_AUTH_URL}?{urlencode(params)}"

def exchange_code_for_token(code: str):
    """Exchange authorization code for access token"""
    if not STRAVA_CLIENT_ID or not STRAVA_CLIENT_SECRET:
        raise Exception("Strava credentials not configured")

    payload = {
        "client_id": STRAVA_CLIENT_ID,
        "client_secret": STRAVA_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
    }

    response = requests.post(STRAVA_TOKEN_URL, data=payload)
    response.raise_for_status()
    return response.json()

def get_athlete_activities(access_token: str, per_page: int = 30):
    """Fetch athlete's recent activities"""
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"per_page": per_page}

    response = requests.get(
        f"{STRAVA_API_BASE}/athlete/activities",
        headers=headers,
        params=params
    )
    response.raise_for_status()
    return response.json()

def refresh_access_token(refresh_token: str):
    """Refresh an expired access token"""
    payload = {
        "client_id": STRAVA_CLIENT_ID,
        "client_secret": STRAVA_CLIENT_SECRET,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }

    response = requests.post(STRAVA_TOKEN_URL, data=payload)
    response.raise_for_status()
    return response.json()
