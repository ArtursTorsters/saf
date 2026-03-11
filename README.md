# SAF Sensor Dashboard

## Build & Run

```bash
docker compose up --build
```

- Frontend: http://localhost:8080
- Backend API: http://localhost:8000/api/sensors
- API Docs: http://localhost:8000/docs

## Stop

```bash
docker compose down
```

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

Vite proxies `/api` requests to `http://localhost:8000`.
