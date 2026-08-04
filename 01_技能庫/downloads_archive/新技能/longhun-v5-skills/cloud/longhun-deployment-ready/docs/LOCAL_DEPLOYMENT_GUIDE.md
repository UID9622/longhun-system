# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# Local Deployment Guide

> **DNA**: `#龍芯⚡️2026-06-19-LONGHUN-DEPLOY-READY-v5.2`  
> **Purpose**: Deploy Longhun system in local/development environment

---

## Quick Start (Local)

For local development, you can use a simplified deployment process.

### Prerequisites

- Python >= 3.9
- pip >= 21.0
- Git

Optional but recommended:
- PostgreSQL >= 13 (or SQLite for simple testing)
- Redis >= 6.0 (or mock for development)

### Step-by-Step Local Deployment

#### 1. Clone Repository

```bash
git clone <repository-url>
cd longhun-deployment-ready
```

#### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
```

#### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with local settings
# For SQLite (simplest):
DATABASE_URL=sqlite:///./local.db
SECRET_KEY=dev-secret-key-change-in-production
APP_ENV=development
LOG_LEVEL=DEBUG
```

#### 5. Initialize Database

```bash
# For SQLite, no external server needed
# Run migrations
alembic upgrade head

# Or if using SQLite without migrations:
python3 -c "from app.database import init_db; init_db()"
```

#### 6. Run Environment Checks

```bash
# Run simplified local checks
python3 scripts/环境验证器.py
python3 scripts/配置验证器.py
```

#### 7. Start Application

```bash
# Development server with auto-reload
python3 -m uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Or use the deployment executor for local
python3 scripts/部署执行器.py --stage service --dry-run
```

#### 8. Verify

```bash
# Health check
curl http://localhost:8000/health

# API documentation (if FastAPI/Flask)
open http://localhost:8000/docs
```

---

## Docker Local Deployment

### Using Docker

```bash
# Build image
docker build -t longhun:local .

# Run container
docker run -d \
  --name longhun-local \
  -p 8000:8000 \
  -e DATABASE_URL=sqlite:///app/local.db \
  -e SECRET_KEY=dev-secret \
  -v $(pwd)/data:/app/data \
  longhun:local

# Check logs
docker logs -f longhun-local
```

### Using Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/longhun
      - SECRET_KEY=dev-secret-key
      - APP_ENV=development
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - ./:/app
    depends_on:
      - db
      - redis

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=longhun
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

volumes:
  postgres_data:
```

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f app

# Run checks inside container
docker-compose exec app python3 scripts/部署就绪检查器.py

# Stop all
docker-compose down

# Clean up
docker-compose down -v
```

---

## Local-Specific Configuration

### SQLite Configuration

For quick local testing without PostgreSQL:

```env
# .env
DATABASE_URL=sqlite:///./local.db
# No external DB server needed
```

### Mock Services

For development without all dependencies:

```python
# config/development.py
USE_MOCK_REDIS = True
USE_MOCK_SMTP = True
DISABLE_AUTH = True  # Only for local dev!
```

### Hot Reload

```bash
# Auto-restart on code changes
python3 -m uvicorn app:app --reload --reload-dir ./app

# Or with watchgod
watchgod app.main
```

---

## Running Tests

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run unit tests
pytest tests/unit/ -v

# Run integration tests
pytest tests/integration/ -v

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test
pytest tests/unit/test_models.py -v -k test_user
```

---

## Debugging

### Enable Debug Mode

```env
APP_ENV=development
DEBUG=true
LOG_LEVEL=DEBUG
```

### PDB Debugging

```python
# Insert in code where needed
import pdb; pdb.set_trace()

# Or use ipdb for better experience
import ipdb; ipdb.set_trace()
```

### Logging

```bash
# View detailed logs
tail -f logs/app.log

# Increase verbosity
LOG_LEVEL=DEBUG python3 -m uvicorn app:app
```

---

## Common Local Issues

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 $(lsof -t -i :8000)

# Or use different port
python3 -m uvicorn app:app --port 8001
```

### Permission Denied

```bash
# Fix permissions
chmod +x scripts/*.py
chmod 600 .env
```

### Module Not Found

```bash
# Ensure virtualenv is activated
which python3  # Should show venv path

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## Local Deployment Checklist

- [ ] Python >= 3.9 installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with local settings
- [ ] Database initialized (SQLite or PostgreSQL running)
- [ ] Application starts without errors
- [ ] Health endpoint responds (`curl localhost:8000/health`)
- [ ] API documentation accessible (`localhost:8000/docs`)

---

**Document DNA**: `#龍芯⚡️2026-06-19-LONGHUN-DEPLOY-READY-v5.2`
