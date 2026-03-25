from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import os
from datetime import datetime
import secrets

from database import get_db, init_db
from models import User, Activity
from strava_client import get_authorization_url, exchange_code_for_token, get_athlete_activities

app = FastAPI(title="Local Legend Finder")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/")
def root():
    return {"message": "Local Legend Finder API", "version": "1.0.0"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

# Strava OAuth endpoints
@app.get("/api/auth/strava")
def strava_auth():
    """Redirect to Strava OAuth authorization page"""
    auth_url = get_authorization_url()
    return {"authorization_url": auth_url}

@app.get("/api/auth/strava/callback")
async def strava_callback(code: str = None, error: str = None, db: Session = Depends(get_db)):
    """Handle Strava OAuth callback"""
    if error:
        raise HTTPException(status_code=400, detail=f"Authorization failed: {error}")

    if not code:
        raise HTTPException(status_code=400, detail="No authorization code provided")

    # Exchange code for token
    token_data = exchange_code_for_token(code)

    # Store or update user in database
    athlete = token_data.get("athlete", {})
    user = db.query(User).filter(User.strava_id == athlete.get("id")).first()

    if not user:
        user = User(
            strava_id=athlete.get("id"),
            username=athlete.get("username"),
            firstname=athlete.get("firstname"),
            lastname=athlete.get("lastname"),
            access_token=token_data.get("access_token"),
            refresh_token=token_data.get("refresh_token"),
            expires_at=token_data.get("expires_at")
        )
        db.add(user)
    else:
        user.access_token = token_data.get("access_token")
        user.refresh_token = token_data.get("refresh_token")
        user.expires_at = token_data.get("expires_at")

    db.commit()

    # Redirect to frontend with success
    return RedirectResponse(url=f"http://localhost:5173?auth=success&user_id={user.id}")

@app.get("/api/user")
def get_user(db: Session = Depends(get_db)):
    """Get current user (mock for now - returns first user or sample data)"""
    user = db.query(User).first()

    if not user:
        # Return sample fallback data
        return {
            "id": 0,
            "username": "demo_user",
            "firstname": "Demo",
            "lastname": "User",
            "is_mock": True
        }

    return {
        "id": user.id,
        "strava_id": user.strava_id,
        "username": user.username,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "is_mock": False
    }

@app.post("/api/sync-activities")
async def sync_activities(db: Session = Depends(get_db)):
    """Sync recent activities from Strava"""
    user = db.query(User).first()

    if not user:
        # Return sample fallback activities
        return {
            "synced": 3,
            "activities": [
                {
                    "id": 1,
                    "name": "Morning Run",
                    "distance": 5000,
                    "moving_time": 1800,
                    "type": "Run",
                    "start_date": "2024-01-15T08:00:00Z"
                },
                {
                    "id": 2,
                    "name": "Evening Ride",
                    "distance": 15000,
                    "moving_time": 2400,
                    "type": "Ride",
                    "start_date": "2024-01-14T18:00:00Z"
                },
                {
                    "id": 3,
                    "name": "Lunch Run",
                    "distance": 3000,
                    "moving_time": 1200,
                    "type": "Run",
                    "start_date": "2024-01-13T12:00:00Z"
                }
            ],
            "is_mock": True
        }

    # Fetch activities from Strava
    activities_data = get_athlete_activities(user.access_token)

    synced_count = 0
    for activity_data in activities_data[:30]:  # Limit to 30 most recent
        activity = db.query(Activity).filter(Activity.strava_id == activity_data.get("id")).first()

        if not activity:
            activity = Activity(
                user_id=user.id,
                strava_id=activity_data.get("id"),
                name=activity_data.get("name"),
                distance=activity_data.get("distance"),
                moving_time=activity_data.get("moving_time"),
                activity_type=activity_data.get("type"),
                start_date=activity_data.get("start_date")
            )
            db.add(activity)
            synced_count += 1

    db.commit()

    return {
        "synced": synced_count,
        "total": len(activities_data),
        "is_mock": False
    }

@app.get("/api/activities")
def get_activities(db: Session = Depends(get_db)):
    """Get all synced activities"""
    user = db.query(User).first()

    if not user:
        # Return sample fallback activities
        return [
            {
                "id": 1,
                "name": "Morning Run",
                "distance": 5000,
                "moving_time": 1800,
                "type": "Run",
                "start_date": "2024-01-15T08:00:00Z",
                "is_mock": True
            },
            {
                "id": 2,
                "name": "Evening Ride",
                "distance": 15000,
                "moving_time": 2400,
                "type": "Ride",
                "start_date": "2024-01-14T18:00:00Z",
                "is_mock": True
            }
        ]

    activities = db.query(Activity).filter(Activity.user_id == user.id).all()

    return [
        {
            "id": activity.id,
            "strava_id": activity.strava_id,
            "name": activity.name,
            "distance": activity.distance,
            "moving_time": activity.moving_time,
            "type": activity.activity_type,
            "start_date": activity.start_date,
            "is_mock": False
        }
        for activity in activities
    ]
