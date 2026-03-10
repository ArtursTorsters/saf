# SAF Sensor Dashboard

A full-stack web application for viewing sensor measurement data.

- **Frontend**: Vue 3 + Vite (served via Nginx)
- **Backend**: Python / FastAPI REST API
- **Containerization**: Docker + Docker Compose

## Architecture

```
┌─────────────────────┐     ┌─────────────────────┐
│  Frontend (:8080)   │     │  Backend  (:8000)    │
│  Vue 3 + Nginx      │────▶│  FastAPI + Uvicorn   │
│                     │ /api│                      │
└─────────────────────┘     └──────────┬───────────┘
                                       │
                                       ▼
                              ┌────────────────┐
                              │  shared_data/  │
                              │  JSON Files    │
                              └────────────────┘
```

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (v20+)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2+)

## Build & Run

```bash
# Clone the repository
git clone https://github.com/<your-username>/saf-sensor-dashboard.git
cd saf-sensor-dashboard

# Build and start containers
docker compose up --build

# The app is now running:
#   Frontend: http://localhost:8080
#   Backend API: http://localhost:8000/api/sensors
#   API Docs: http://localhost:8000/docs
```

### Stop

```bash
docker compose down
```

## Features

- **Sensor data table** with all sensor measurements
- **Sort** any column (ascending / descending) by clicking headers
- **Search** sensors by name in real-time
- **Filter** by sensor type via dropdown
- **Toggle metric columns** — show/hide individual metrics
- **Missing data handling** — graceful fallbacks for missing names, types, and metrics

## Project Structure

```
SAF/
├── backend/                  # Python FastAPI backend
│   ├── app/
│   │   ├── main.py           # App entry point (CORS, lifespan)
│   │   ├── api/
│   │   │   └── sensors.py    # GET /api/sensors endpoint
│   │   └── services/
│   │       └── data_service.py  # Data loading & merging logic
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                 # Vue 3 + Vite frontend
│   ├── src/
│   │   ├── main.js           # Vue app entry
│   │   ├── App.vue           # Root component
│   │   ├── components/
│   │   │   └── SensorTable.vue  # Interactive data table
│   │   ├── composables/
│   │   │   └── useSensors.js    # Table state & logic
│   │   └── services/
│   │       └── api.js           # API fetch wrapper
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
├── shared_data/              # JSON data files
│   ├── sensors.json
│   ├── metrics.json
│   └── sensorTypes.json
├── docker-compose.yml
└── README.md
```

## Data Format

See `shared_data/` for the JSON file structure. The backend merges all three files and serves a flat, table-ready response.

## Development (without Docker)

### Backend
```bash
cd backend
pip install -r requirements.txt
DATA_DIR=../shared_data uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

The Vite dev server proxies `/api` requests to `http://localhost:8000`.
# saf
