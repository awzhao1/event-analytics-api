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
## Environment Variables
create a `.env` file in the root of the project:
```
# Main DB
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/event_analytics

# Test DB
TEST_DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/event_analytics_test
```
## Development (Local)
Start virtual environment and install dependencies:
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Start the FastAPI app:
```
uvicorn app.main:app --reload
```
Visit http://127.0.0.1:8000/docs for the Swagger UI.

## Docker Setup
### Build and run the app
```
docker compose up --build
```
### Run tests in Docker
```
docker compose run tests
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
  -d `{"event_type": "page_view", "event_metadata": {"page": "/home"}}`
```
## Testing
Run tests locally (uses SQLite by default):
```
pytest -v
```
## Contributing
1. Fork the repo
2. Create a feature branch
3. Commit changes
4. Open a pull request

