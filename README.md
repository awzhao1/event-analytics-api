# Event Analytics API
A FastAPI-based API for tracking user events with analytics support. Includes Docker support, PostgreSQL integration, and automated tests.
### Features
- Record user events(e.g., `page_view`, `signup`, etc.)
- Event summary with time range filtering
- API key authentication per user
- PostgreSQL database with Alembic migrations
- Fully Dockerized for development and testing
- Automated tests with `pytest`

## Getting Started
### Prerequisites
- Python 3.14+
- Docker & Docker Compose

### Clone the repository
```
git clone <url>
cd event-analytics-api
```

## Development (Local)
Start virtual environment and install dependencies:
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Start PostgreSQL.

Create the required database in PostgreSQL:
```
psql -U postgres
CREATE DATABASE event_analytics;
```
Create a `.env` file in the root of the project:
```
# Main DB
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/event_analytics
```
Run Alembic migrations to create tables
```
alembic upgrade head
```
Start the FastAPI app:
```
uvicorn app.main:app --reload
```
Visit http://127.0.0.1:8000/docs for the Swagger UI.

## Docker Setup
### Environment Variables
Create a `.env` file in the root of the project:
```
# Main DB
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/event_analytics
```
Note that this is different from the local `.env` file
### Build and run the app
```
docker compose up --build
```

## AWS Deployment (EC2)
### High Level Steps:
1. Launch an EC2 instance (Amazon Linux)
2. Download Docker
3. Clone this repository
4. Create .env file in server
5. Run:
```
docker compose up -d --build
```
### Open Required Ports
In EC2 security group:
- 8000 - API access
- 22 -SSH
### Access the API
```
http://<EC2_PUBLIC_IP>:8000/docs
```
## API Usage
### Authentication
- Each user has an `api_key`
- Include `X-API-Key` header in requests
### Endpoints
- `POST /events/` - Create an event
- `GET /events/summary` - Get event summary (supports `start` and `end` time parameters)
Example request:
```
curl -X POST http://127.0.0.1:8000/events/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key_here" \
  -d '{"event_type": "page_view", "event_metadata": {"page": "/home"}}'
```
## Testing
Run tests locally (uses SQLite by default):
```
pytest -v
```

Run tests in Docker
```
docker compose run tests
```

## Architecture
Systems:
```mermaid
graph TD;
Client-->FastAPI;
FastAPI-->PostgreSQL;
```
## Contributing
1. Fork the repo
2. Create a feature branch
3. Commit changes
4. Open a pull request

