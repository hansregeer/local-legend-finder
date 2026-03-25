# 🏆 Local Legend Finder

A Strava-powered app to track your activities and find local legends. Built with FastAPI backend and React frontend.

## 🚀 Features

- **Strava OAuth Integration** - Secure authentication with Strava
- **Activity Sync** - Automatically sync your recent activities
- **Mock Data Support** - Works without Strava credentials using sample data
- **Modern UI** - Clean, responsive interface built with React + TypeScript
- **Docker Ready** - Easy deployment with Docker Compose

## 📁 Project Structure

```
local-legend-finder/
├── backend/                # FastAPI backend
│   ├── main.py            # API endpoints
│   ├── database.py        # Database configuration
│   ├── models.py          # SQLAlchemy models
│   ├── strava_client.py   # Strava API client
│   ├── requirements.txt   # Python dependencies
│   ├── Dockerfile         # Backend Docker config
│   └── .env.example       # Environment variables template
├── frontend/              # React frontend
│   ├── src/
│   │   ├── App.tsx        # Main application component
│   │   ├── App.css        # Application styles
│   │   └── main.tsx       # Application entry point
│   ├── package.json       # Node dependencies
│   ├── vite.config.ts     # Vite configuration
│   ├── Dockerfile         # Frontend Docker config
│   ├── nginx.conf         # Nginx configuration
│   └── .env.example       # Environment variables template
├── docker-compose.yml     # Docker orchestration
└── README.md             # This file
```

## 🛠️ Prerequisites

- Python 3.11 - 3.13 (⚠️ Python 3.14+ not yet supported by Pydantic)
- Node.js 20+
- npm or yarn
- Docker & Docker Compose (optional)

## 📋 Setup

### 1. Get Strava API Credentials (Optional)

The app works with mock data, but for real Strava integration:

1. Go to https://www.strava.com/settings/api
2. Create a new application
3. Note your **Client ID** and **Client Secret**
4. Set Authorization Callback Domain to: `localhost`

### 2. Configure Environment Variables

**Backend:**
```bash
cd backend
cp .env.example .env
# Edit .env with your Strava credentials (or leave as-is for mock mode)
```

**Frontend:**
```bash
cd frontend
cp .env.example .env
# Optional: customize API URL if needed
```

**Root (for Docker):**
```bash
cp .env.example .env
# Edit .env with your Strava credentials (or leave as-is for mock mode)
```

## 🚀 Running the Application

### Option 1: Local Development (Recommended for development)

**Terminal 1 - Backend:**
```bash
cd backend

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Access the app at: **http://localhost:5173**

### Option 2: Docker Compose (Recommended for deployment)

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

Access the app at: **http://localhost:3000**

To stop:
```bash
docker-compose down
```

## 🎯 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info |
| `/api/health` | GET | Health check |
| `/api/auth/strava` | GET | Get Strava OAuth URL |
| `/api/auth/strava/callback` | GET | OAuth callback handler |
| `/api/user` | GET | Get current user info |
| `/api/sync-activities` | POST | Sync activities from Strava |
| `/api/activities` | GET | Get all synced activities |

## 📊 Database

The app uses SQLite for local development. The database file (`local_legend.db`) is created automatically on first run.

**Models:**
- **User** - Strava user information and tokens
- **Activity** - Synced Strava activities

## 🔧 Development

### Backend Development

```bash
cd backend

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn main:app --reload --port 8000
```

### Frontend Development

```bash
cd frontend
npm install

# Development server with hot reload
npm run dev

# Type checking
npm run build
```

## ✅ Mock Data

The app includes fallback sample data so you can explore the UI without Strava credentials:

- **Demo User**: Shows when no Strava account is connected
- **Sample Activities**: 3 mock activities (runs and rides)
- **Full Functionality**: All UI features work with mock data

## 🐛 Troubleshooting

**Backend won't start:**
- Check Python version: `python --version` (need 3.11+)
- Install dependencies: `pip install -r requirements.txt`
- Check port 8000 is available

**Frontend won't start:**
- Check Node version: `node --version` (need 20+)
- Clear node_modules: `rm -rf node_modules && npm install`
- Check port 5173 is available

**Strava OAuth not working:**
- Verify callback URL in Strava API settings matches `.env`
- Check client ID and secret are correct
- Ensure authorization callback domain is set to `localhost`

**Docker issues:**
- Check Docker is running: `docker --version`
- Clear containers: `docker-compose down -v`
- Rebuild: `docker-compose up --build`

## 📝 TODO / Mocked Parts

### Currently Mocked
- ✅ User authentication (returns first user or demo user)
- ✅ Sample fallback activities when no Strava connection
- ✅ Basic activity display

### Next Steps
1. **Authentication**: Implement proper session management
2. **Local Legends**: Add segment analysis to find local legends
3. **Leaderboards**: Show segment leaderboards
4. **Maps**: Display activity routes on maps
5. **Filtering**: Add activity type and date filters
6. **Statistics**: Add personal stats dashboard
7. **Token Refresh**: Implement automatic Strava token refresh
8. **Error Handling**: Add comprehensive error handling and user feedback
9. **Tests**: Add unit and integration tests
10. **Postgres**: Migrate to PostgreSQL for production

## 🤝 Contributing

This is an MVP project. Future enhancements coming soon!

## 📄 License

MIT

## 🙏 Acknowledgments

- Powered by [Strava API](https://developers.strava.com/)
- Built with [FastAPI](https://fastapi.tiangolo.com/)
- UI built with [React](https://react.dev/) + [Vite](https://vitejs.dev/)
