# Event System

## Prerequisites

- Python 3.13+
- Poetry 2.1.1
- Docker and Docker Compose
- PostgreSQL 15+

The services are ran with `docker-compose up -d` command.
If running on a windows machine, use wsl2.

## Setup

1. Clone the repository:
```bash
git clone https://github.com/tiwaz3d/Event-System.git
cd Event-System
```

2. Install Poetry:
   
(Required if dependencies need to be added otherwise docker-build takes care of this step
Same goes for steps 3 and 4 )
```bash
sudo apt update && sudo apt install curl python3-venv -y
curl -sSL https://install.python-poetry.org | python3 -
# or
sudo apt install python3-poetry
```

3. Verify Poetry installation:
```bash
poetry --version
```

4. Install dependencies:
```bash
poetry install
```

5. Install Docker and Docker Compose:
```bash
sudo apt update
sudo apt install docker.io -y

sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose
```

6. Set up the `.env` file:
Create a file at `Event-System/event_system/.env` with the following content:
```env
EVENT_CONSUMER_POSTGRES_DB=event_system
EVENT_CONSUMER_POSTGRES_USER=admin
EVENT_CONSUMER_POSTGRES_PASSWORD=secret
EVENT_CONSUMER_DATABASE_URL=postgresql+asyncpg://admin:secret@event_system_db:5432/event_system
EVENT_CONSUMER_PORT=8000
EVENT_PROPAGATOR_INTERVAL=5
EVENT_PROPAGATOR_TARGET_URL=http://consumer:8000/event
EVENT_PROPAGATOR_EVENTS_FILE=event_system/events.json
```

7. Apply database migrations:
```bash
poetry run alembic upgrade head
```

8. Start the services:
```bash
docker-compose build
docker-compose up -d

# To shut down
docker-compose down
```

9. [Optional] Logs for the services can be seen with:
```bash
docker-compose logs -f

# For a specific container:
# docker-compose logs <container> -f
```

## Configuration

All configuration can be changed/set in the .env file:

- `EVENT_PROPAGATOR_INTERVAL`: Time between events in seconds
- `EVENT_PROPAGATOR_TARGET_URL`: URL to send events to
- `EVENT_PROPAGATOR_EVENTS_FILE`: Path to events file
- `EVENT_CONSUMER_PORT`: Port for the consumer service
- `EVENT_CONSUMER_DATABASE_URL`: PostgreSQL connection string

## API Documentation

Once running, access the API documentation at:
- Health check: http://localhost:8000/health
- Consumer Service: http://localhost:8000/docs
- Metrics: http://localhost:8000/metrics

## License

[MIT License](LICENSE)

### .gitignore

```gitignore
# Virtual Environment
.env
.venv
env/
venv/
ENV/

# Poetry
poetry.lock

# IDE
.idea/
.vscode/
*.swp
*.swo

# Test
.pytest_cache/

# Logs
*.log

# Python cache files
__pycache__/
*.py[cod]
*$py.class
.python-version
```
