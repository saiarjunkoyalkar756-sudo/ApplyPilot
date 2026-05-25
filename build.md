# Build Guide: Job Copilot — Production-Grade AI Job Application Platform

> **Version:** 1.0.0  
> **Last Updated:** 2026-05-25  
> **Status:** Phase 1 — MVP Development  
> **Estimated Build Time:** 120-160 hours (Phase 1)

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture Diagram](#2-architecture-diagram)
3. [Technology Stack](#3-technology-stack)
4. [Development Environment Setup](#4-development-environment-setup)
5. [Phase 1: MVP Implementation](#5-phase-1-mvp-implementation)
6. [Phase 2: Product-Market Fit](#6-phase-2-product-market-fit)
7. [Phase 3: Scale](#7-phase-3-scale)
8. [Phase 4: Enterprise](#8-phase-4-enterprise)
9. [Database Schema](#9-database-schema)
10. [API Specification](#10-api-specification)
11. [Testing Strategy](#11-testing-strategy)
12. [Deployment Guide](#12-deployment-guide)
13. [Monitoring & Observability](#13-monitoring--observability)
14. [Security Checklist](#14-security-checklist)
15. [Troubleshooting](#15-troubleshooting)

---

## 1. Project Overview

**Job Copilot** is an AI-powered job application automation platform that:
- Parses resumes using AI (PDF/DOCX to structured JSON)
- Scrapes job boards (Indeed, LinkedIn, Greenhouse, Lever)
- Scores job matches using semantic + structured algorithms
- Generates tailored resumes and cover letters per job
- Automates browser-based applications with human-in-the-loop approval
- Tracks application pipeline and analytics

**Target Users:** Job seekers, career coaches, university career centers, bootcamp graduates

**Business Model:** Freemium SaaS (Free to Pro $29/mo to Business $99/mo to Enterprise custom)

---

## 2. Architecture Diagram

```
Client Layer:
- Next.js Web App (SSR, App Router)
- Browser Extension (Chrome/Firefox)
- Mobile PWA (Future)

API Gateway:
- Kong or AWS API Gateway
- Rate limiting, auth, routing

Microservices (Kubernetes):
- Auth Service (FastAPI)
- Parser Service (FastAPI)
- Scraper Service (FastAPI)
- Matcher Service (FastAPI)
- Resume Builder Service (FastAPI)
- Applier Service (FastAPI)
- Billing Service (FastAPI)
- Notification Service (FastAPI)

Message Queue:
- RabbitMQ / Redis Streams
- Async job processing

Data & Storage:
- PostgreSQL 16 (Primary)
- Redis (Cache/Sessions)
- Elasticsearch 8 (Search)
- Qdrant (Vector DB)
- S3/MinIO (Object Storage)
- ClickHouse (Analytics)

AI/ML:
- OpenAI GPT-4o / Claude 3.5
- Self-hosted models (Future)
- Vector embeddings for matching
```

---

## 3. Technology Stack

### 3.1 Core Services

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Frontend | Next.js | 14.x | SSR, React Server Components |
| | TypeScript | 5.3+ | Type safety |
| | Tailwind CSS | 3.4+ | Utility-first styling |
| | shadcn/ui | Latest | Component library |
| | Framer Motion | 11.x | Animations |
| | React Query | 5.x | Server state |
| | Zustand | 4.x | Client state |
| API Gateway | Kong | 3.x | Rate limiting, auth |
| Backend | FastAPI | 0.110+ | Python microservices |
| | Go | 1.22+ | Performance-critical paths |
| | Uvicorn | 0.29+ | ASGI server |
| | Celery | 5.3+ | Distributed task queue |
| Database | PostgreSQL | 16.x | Primary database |
| | Redis | 7.2+ | Cache, sessions, Celery |
| | Elasticsearch | 8.12+ | Full-text search |
| | Qdrant | 1.7+ | Vector database |
| | ClickHouse | 24.x | Analytics warehouse |
| Storage | AWS S3 / MinIO | Latest | Resume PDFs |
| Message Queue | RabbitMQ | 3.12+ | Async processing |
| Browser Automation | Playwright | 1.42+ | Browser control |
| | Playwright Cluster | Latest | Distributed nodes |
| AI/ML | OpenAI API | Latest | GPT-4o, embeddings |
| | LangChain | 0.1.x | LLM orchestration |
| Infrastructure | Docker | 25.x+ | Containerization |
| | Kubernetes | 1.29+ | Orchestration |
| | Terraform | 1.7+ | IaC |
| | Helm | 3.14+ | K8s packages |
| | GitHub Actions | N/A | CI/CD |
| Monitoring | Prometheus | 2.50+ | Metrics |
| | Grafana | 10.3+ | Visualization |
| | Loki | 2.9+ | Log aggregation |
| | Jaeger | 1.55+ | Distributed tracing |
| | PagerDuty | N/A | Incident management |
| Payments | Stripe | Latest | Subscription billing |

### 3.2 Python Dependencies

```txt
# Core Framework
fastapi==0.110.0
uvicorn[standard]==0.29.0
python-multipart==0.0.9
pydantic==2.6.4
pydantic-settings==2.2.1
email-validator==2.1.1

# Authentication & Security
python-jose[cryptography]==3.3.0
passlib[argon2]==1.7.4
python-dotenv==1.0.1
cryptography==42.0.5
pyotp==2.9.0

# Database & ORM
sqlalchemy==2.0.28
alembic==1.13.1
asyncpg==0.29.0
psycopg2-binary==2.9.9
redis==5.0.3

# Search & Vector
elasticsearch==8.12.1
qdrant-client==1.8.0
pgvector==0.2.5

# Message Queue
celery==5.3.6
kombu==5.3.6
amqp==5.2.0

# AI / LLM
openai==1.14.2
anthropic==0.21.3
langchain==0.1.12
langchain-openai==0.0.8
tiktoken==0.6.0

# Resume Parsing
pdfplumber==0.11.0
python-docx==1.1.2
PyMuPDF==1.23.26

# PDF Generation
reportlab==4.1.0
weasyprint==61.2
Jinja2==3.1.3

# Browser Automation
playwright==1.42.0
playwright-stealth==1.0.6
undetected-playwright==0.0.1

# Web Scraping
beautifulsoup4==4.12.3
lxml==5.1.0
requests==2.31.0
httpx==0.27.0
aiohttp==3.9.3

# Data Processing
pandas==2.2.1
numpy==1.26.4
scikit-learn==1.4.1
scipy==1.12.0

# Utilities
python-slugify==8.0.4
Pillow==10.2.0
python-magic==0.4.27
tenacity==8.2.3
structlog==24.1.0

# Testing
pytest==8.1.1
pytest-asyncio==0.23.5
pytest-cov==5.0.0
factory-boy==3.3.0
faker==24.4.0

# Development
black==24.3.0
isort==5.13.2
flake8==7.0.0
mypy==1.9.0
pre-commit==3.7.0
```

### 3.3 Node.js Dependencies (Frontend)

```json
{
  "dependencies": {
    "next": "^14.1.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "typescript": "^5.3.3",
    "tailwindcss": "^3.4.1",
    "@tailwindcss/forms": "^0.5.7",
    "@tailwindcss/typography": "^0.5.10",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.0",
    "lucide-react": "^0.344.0",
    "framer-motion": "^11.0.0",
    "@tanstack/react-query": "^5.24.0",
    "zustand": "^4.5.0",
    "axios": "^1.6.7",
    "react-hook-form": "^7.51.0",
    "@hookform/resolvers": "^3.3.4",
    "zod": "^3.22.4",
    "react-hot-toast": "^2.4.1",
    "date-fns": "^3.3.1",
    "recharts": "^2.12.0",
    "@radix-ui/react-dialog": "^1.0.5",
    "@radix-ui/react-dropdown-menu": "^2.0.6",
    "@radix-ui/react-select": "^2.0.0",
    "@radix-ui/react-tabs": "^1.0.4",
    "@radix-ui/react-toast": "^1.1.5",
    "@radix-ui/react-tooltip": "^1.0.7",
    "@stripe/stripe-js": "^3.0.0",
    "@stripe/react-stripe-js": "^2.5.0",
    "socket.io-client": "^4.7.4",
    "react-dropzone": "^14.2.3",
    "react-pdf": "^7.7.1",
    "react-markdown": "^9.0.1"
  },
  "devDependencies": {
    "eslint": "^8.57.0",
    "eslint-config-next": "^14.1.0",
    "prettier": "^3.2.5",
    "jest": "^29.7.0",
    "@testing-library/react": "^14.2.0",
    "@testing-library/jest-dom": "^6.4.0",
    "cypress": "^13.6.0"
  }
}
```

---

## 4. Development Environment Setup

### 4.1 Prerequisites

| Tool | Version | Installation |
|------|---------|-------------|
| Python | 3.11+ | pyenv install 3.11.8 |
| Node.js | 20.x LTS | nvm install 20 |
| Docker | 25.x+ | docker.com |
| Docker Compose | 2.24+ | Included with Docker |
| Terraform | 1.7+ | brew install terraform |
| kubectl | 1.29+ | brew install kubectl |
| Helm | 3.14+ | brew install helm |
| Git | 2.43+ | brew install git |
| Make | Latest | brew install make |

### 4.2 Repository Setup

```bash
# 1. Clone repository
git clone https://github.com/your-org/job-copilot.git
cd job-copilot

# 2. Create environment files
cp .env.example .env
cp .env.example .env.local

# 3. Edit .env with your keys
# OPENAI_API_KEY=sk-...
# STRIPE_SECRET_KEY=sk_test_...
# DATABASE_URL=postgresql://...

# 4. Initialize Python environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 5. Initialize frontend
cd frontend
npm install

# 6. Install Playwright browsers
cd ..
playwright install chromium

# 7. Start infrastructure
docker-compose -f docker-compose.dev.yml up -d

# 8. Run database migrations
alembic upgrade head

# 9. Seed development data
python scripts/seed_dev_data.py

# 10. Start services (in separate terminals)
make start-auth
make start-parser
make start-scraper
make start-matcher
make start-resume-builder
make start-applier
make start-frontend
make start-workers
```

### 4.3 Docker Compose (Development)

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: jobcopilot
      POSTGRES_PASSWORD: devpassword
      POSTGRES_DB: jobcopilot_dev
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U jobcopilot"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

  elasticsearch:
    image: elasticsearch:8.12.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9200:9200"
    volumes:
      - es_data:/usr/share/elasticsearch/data

  qdrant:
    image: qdrant/qdrant:v1.8.0
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage

  rabbitmq:
    image: rabbitmq:3.12-management-alpine
    ports:
      - "5672:5672"
      - "15672:15672"
    environment:
      RABBITMQ_DEFAULT_USER: jobcopilot
      RABBITMQ_DEFAULT_PASS: devpassword
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq

  minio:
    image: minio/minio:latest
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    volumes:
      - minio_data:/data
    command: server /data --console-address ":9001"

  mailhog:
    image: mailhog/mailhog:latest
    ports:
      - "1025:1025"
      - "8025:8025"

volumes:
  postgres_data:
  redis_data:
  es_data:
  qdrant_data:
  rabbitmq_data:
  minio_data:
```

### 4.4 Makefile Commands

```makefile
.PHONY: help install start stop test lint format migrate seed clean

help:
	@echo "Job Copilot Development Commands"
	@echo "install         - Install all dependencies"
	@echo "start           - Start all services with docker-compose"
	@echo "stop            - Stop all services"
	@echo "start-auth      - Start auth service"
	@echo "start-parser    - Start parser service"
	@echo "start-scraper   - Start scraper service"
	@echo "start-matcher   - Start matcher service"
	@echo "start-resume    - Start resume builder service"
	@echo "start-applier   - Start applier service"
	@echo "start-workers   - Start Celery workers"
	@echo "start-frontend  - Start Next.js dev server"
	@echo "test            - Run all tests"
	@echo "lint            - Run linters"
	@echo "format          - Format all code"
	@echo "migrate         - Run database migrations"
	@echo "migrate-make    - Create new migration"
	@echo "seed            - Seed development data"
	@echo "clean           - Clean build artifacts"

install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	cd frontend && npm install
	playwright install chromium

start:
	docker-compose -f docker-compose.dev.yml up -d
	@echo "Services started. Run 'make migrate' and 'make seed' if first time."

stop:
	docker-compose -f docker-compose.dev.yml down

start-auth:
	cd services/auth && uvicorn main:app --reload --port 8001

start-parser:
	cd services/parser && uvicorn main:app --reload --port 8002

start-scraper:
	cd services/scraper && uvicorn main:app --reload --port 8003

start-matcher:
	cd services/matcher && uvicorn main:app --reload --port 8004

start-resume:
	cd services/resume-builder && uvicorn main:app --reload --port 8005

start-applier:
	cd services/applier && uvicorn main:app --reload --port 8006

start-workers:
	celery -A services.shared.celery_app worker --loglevel=info

start-frontend:
	cd frontend && npm run dev

test:
	pytest --cov=services --cov-report=term-missing

test-unit:
	pytest -m unit

test-integration:
	pytest -m integration

test-e2e:
	cd frontend && npm run cypress:run

lint:
	flake8 services
	mypy services
	cd frontend && npm run lint

format:
	black services
	isort services
	cd frontend && npm run format

migrate:
	alembic upgrade head

migrate-make:
	@read -p "Migration message: " msg; alembic revision --autogenerate -m "$$msg"

seed:
	python scripts/seed_dev_data.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf htmlcov .pytest_cache
	cd frontend && rm -rf .next node_modules
```

---

## 5. Phase 1: MVP Implementation (Weeks 1-4)

### 5.1 Goals
- Single-user system (no multi-tenancy yet)
- Resume upload + AI parsing
- Indeed scraper only
- Basic matching (keyword-based)
- Manual application assistant (browser opens, user fills)
- Simple Streamlit-like UI in Next.js
- SQLite database (upgrade to PostgreSQL in Phase 2)

### 5.2 Week 1: Foundation

**Day 1-2: Project Structure & Dev Environment**
- [ ] Set up monorepo structure
- [ ] Docker Compose for local dev
- [ ] Pre-commit hooks (black, isort, flake8, mypy)
- [ ] CI pipeline (GitHub Actions: lint + test on PR)

**Day 3-4: Database & Models**
- [ ] SQLAlchemy models (simplified Phase 1 schema)
- [ ] Alembic migrations
- [ ] Pydantic schemas for API validation
- [ ] Seed script with sample data

**Day 5-7: Resume Parser**
- [ ] PDF text extraction (pdfplumber)
- [ ] DOCX text extraction (python-docx)
- [ ] OpenAI structured output parsing
- [ ] Save to database + file system
- [ ] API endpoint: POST /api/v1/resumes/upload
- [ ] Frontend: Upload component with progress

### 5.3 Week 2: Job Discovery

**Day 8-10: Indeed Scraper**
- [ ] Playwright stealth browser setup
- [ ] Search URL construction
- [ ] Job card extraction (title, company, location, URL)
- [ ] Pagination handling
- [ ] Anti-detection basics (delays, user agents)
- [ ] Store to database
- [ ] API endpoint: POST /api/v1/scraper/jobs/search

**Day 11-12: Job Storage & API**
- [ ] Job CRUD API endpoints
- [ ] Filtering, pagination
- [ ] Frontend: Job listing table

**Day 13-14: Matching Engine v1**
- [ ] Keyword-based skill matching
- [ ] Simple score calculation (0-100)
- [ ] API endpoint: POST /api/v1/matches/generate
- [ ] Frontend: Match results with scores

### 5.4 Week 3: Application Assistant

**Day 15-17: Browser Automation**
- [ ] Playwright browser launcher (visible mode)
- [ ] Greenhouse form detection (heuristic)
- [ ] Field filling: name, email, phone
- [ ] Screenshot capture at each step
- [ ] Human approval gate (pause before submit)
- [ ] API endpoint: POST /api/v1/applications

**Day 18-19: Resume Tailoring v1**
- [ ] OpenAI prompt for resume rewriting
- [ ] Simple text output (not PDF yet)
- [ ] Cover letter generation
- [ ] API endpoint: POST /api/v1/resumes/{id}/tailor

**Day 20-21: Application Tracking**
- [ ] Application status model
- [ ] Pipeline view (Kanban)
- [ ] API endpoints for status updates
- [ ] Frontend: Pipeline board

### 5.5 Week 4: UI Polish & Integration

**Day 22-24: Next.js Dashboard**
- [ ] Sidebar navigation
- [ ] Resume upload page
- [ ] Job matches page with actions
- [ ] Application pipeline page
- [ ] Settings page

**Day 25-26: Real-time Updates**
- [ ] WebSocket connection for application progress
- [ ] Screenshot streaming
- [ ] Status notifications

**Day 27-28: Testing & Bug Fixes**
- [ ] Unit tests for parser, matcher
- [ ] Integration tests for scraper
- [ ] E2E test: upload resume to find matches to start application
- [ ] Performance profiling

### 5.6 Phase 1 Database Schema (Simplified)

```sql
-- Phase 1: Single-user, no multi-tenancy

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE resumes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    filename VARCHAR(255),
    storage_path VARCHAR(500),
    parsed_data JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    description TEXT,
    url VARCHAR(500) NOT NULL,
    source VARCHAR(50) DEFAULT 'indeed',
    posted_date DATE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE matches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    resume_id UUID REFERENCES resumes(id),
    job_id UUID REFERENCES jobs(id),
    match_score FLOAT NOT NULL,
    status VARCHAR(20) DEFAULT 'new',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, resume_id, job_id)
);

CREATE TABLE applications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    match_id UUID REFERENCES matches(id),
    job_id UUID REFERENCES jobs(id),
    status VARCHAR(50) DEFAULT 'draft',
    screenshots JSONB DEFAULT '[]',
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## 6. Phase 2: Product-Market Fit (Weeks 5-8)

### 6.1 Goals
- Multi-tenancy (teams/organizations)
- LinkedIn + Greenhouse scrapers
- Semantic matching (vector search)
- PDF resume generation
- Stripe billing (Free, Pro, Business tiers)
- Advanced analytics dashboard

### 6.2 Key Additions

| Feature | Implementation |
|---------|---------------|
| Multi-tenancy | tenant_id on all tables, row-level security |
| LinkedIn Scraper | Cookie-based auth, stealth mode, rate limiting |
| Greenhouse API | Official API integration where available |
| Vector Matching | OpenAI embeddings + Qdrant cosine similarity |
| PDF Generation | ReportLab/WeasyPrint with professional templates |
| Stripe Billing | Checkout, portal, webhooks, usage tracking |
| Analytics | Response rate tracking, A/B testing framework |

---

## 7. Phase 3: Scale (Weeks 9-16)

### 7.1 Goals
- Microservices architecture
- Distributed Playwright cluster
- Elasticsearch for job search
- Redis caching layer
- Kubernetes deployment
- Advanced anti-detection

### 7.2 Infrastructure Changes

Before (Phase 1-2):          After (Phase 3):
- Monolithic FastAPI         - 6 independent services
- SQLite/PostgreSQL          - PostgreSQL + Redis + Elasticsearch
- Local Playwright           - Playwright Cluster (3-10 nodes)
- Single server              - Kubernetes (EKS/GKE)
- Manual deploy              - GitHub Actions + Terraform

---

## 8. Phase 4: Enterprise (Weeks 17-24)

### 8.1 Goals
- SAML/SSO integration
- Audit logs and compliance
- Custom integrations (Workday, SAP SuccessFactors)
- Dedicated account management
- SOC 2 Type II certification
- White-label options

---

## 9. Database Schema

### 9.1 Complete Production Schema

See the full schema in the architecture section. Key design principles:

1. Multi-tenancy: Every table has tenant_id for B2B
2. Soft deletes: deleted_at timestamp, never hard delete
3. Versioning: Resume versions, application status history
4. Audit: Separate audit_logs table with immutable records
5. JSONB flexibility: Metadata fields for source-specific data
6. Vector embeddings: pgvector extension for similarity search

### 9.2 Migration Strategy

```bash
# Create migration
make migrate-make
# Enter description: "add tenant support"

# Edit generated file in alembic/versions/
# Add upgrade/downgrade logic

# Apply migration
make migrate

# Rollback (if needed)
alembic downgrade -1
```

---

## 10. API Specification

### 10.1 Authentication

```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe"
}

Response: 201 Created
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJSUzI1NiIs...",
  "expires_in": 900,
  "token_type": "Bearer"
}
```

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!"
}

Response: 200 OK
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJSUzI1NiIs...",
  "expires_in": 900,
  "token_type": "Bearer"
}
```

### 10.2 Resume Upload

```http
POST /api/v1/resumes/upload
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <resume.pdf>
parse_immediately: true

Response: 202 Accepted
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "parsing",
  "upload_url": "https://s3.../resume.pdf",
  "check_status_url": "/api/v1/resumes/550e8400-e29b-41d4-a716-446655440000/status"
}
```

### 10.3 Job Search

```http
POST /api/v1/scraper/jobs/search
Authorization: Bearer <token>
Content-Type: application/json

{
  "boards": ["indeed", "linkedin"],
  "keywords": "Software Engineer",
  "location": "San Francisco, CA",
  "remote": true,
  "experience_level": "mid",
  "salary_min": 120000,
  "salary_max": 200000,
  "days_posted": 7
}

Response: 202 Accepted
{
  "job_id": "job-123-abc",
  "status": "queued",
  "estimated_completion": "2026-05-25T16:00:00Z"
}
```

### 10.4 Get Matches

```http
GET /api/v1/matches?min_score=70&limit=20&offset=0
Authorization: Bearer <token>

Response: 200 OK
{
  "total": 156,
  "matches": [
    {
      "id": "match-001",
      "job": {
        "id": "job-001",
        "title": "Senior Frontend Engineer",
        "company": "Stripe",
        "location": "Remote",
        "salary": "$150k-$200k",
        "url": "https://..."
      },
      "match_score": 92,
      "skill_match": 95,
      "experience_match": 90,
      "explanation": "Excellent match: You have 8/9 required skills...",
      "missing_skills": ["GraphQL"],
      "suggested_changes": ["Emphasize your REST API experience"]
    }
  ]
}
```

### 10.5 Start Application

```http
POST /api/v1/applications
Authorization: Bearer <token>
Content-Type: application/json

{
  "match_id": "match-001",
  "auto_submit": false,
  "generate_tailored_resume": true,
  "generate_cover_letter": true
}

Response: 201 Created
{
  "id": "app-001",
  "status": "queued",
  "websocket_url": "wss://api.jobcopilot.io/ws/applications/app-001",
  "estimated_start": "2026-05-25T15:20:00Z"
}
```

### 10.6 WebSocket Updates

```json
{
  "type": "status_update",
  "application_id": "app-001",
  "status": "filling_form",
  "progress": 65,
  "message": "Filling work experience section...",
  "screenshot_url": "https://s3.../screenshot_3.png",
  "timestamp": "2026-05-25T15:18:30Z"
}
```

### 10.7 Approve Application

```http
POST /api/v1/applications/app-001/approve
Authorization: Bearer <token>
Content-Type: application/json

{
  "approved": true,
  "notes": "Looks good, submit it"
}

Response: 200 OK
{
  "id": "app-001",
  "status": "submitted",
  "submitted_at": "2026-05-25T15:19:00Z",
  "confirmation": "Application ID: GH-12345"
}
```

---

## 11. Testing Strategy

### 11.1 Test Pyramid

```
        /\
       /  \
      / E2E \      <- Cypress (5%)
     /─────────\
    / Integration \   <- API tests, DB tests (15%)
   /─────────────────\
  /      Unit          \ <- Pytest, Jest (80%)
 /─────────────────────────\
```

### 11.2 Unit Tests

```python
# tests/test_parser.py
import pytest
from services.parser import ResumeParser

@pytest.fixture
def parser():
    return ResumeParser()

@pytest.fixture
def sample_pdf():
    return "tests/fixtures/sample_resume.pdf"

def test_parse_pdf(parser, sample_pdf):
    result = parser.parse(sample_pdf)
    assert result["name"] == "John Doe"
    assert "john@email.com" in result["email"]
    assert "Python" in result["skills"]
    assert len(result["experience"]) >= 1

def test_parse_invalid_file(parser):
    with pytest.raises(ValueError, match="Unsupported file format"):
        parser.parse("tests/fixtures/image.jpg")

def test_parse_empty_pdf(parser):
    with pytest.raises(ValueError, match="No text content found"):
        parser.parse("tests/fixtures/empty.pdf")
```

### 11.3 Integration Tests

```python
# tests/integration/test_scraper.py
import pytest
from fastapi.testclient import TestClient
from services.scraper.main import app

client = TestClient(app)

@pytest.mark.integration
@pytest.mark.asyncio
async def test_scrape_indeed():
    response = client.post("/api/v1/scraper/jobs/search", json={
        "boards": ["indeed"],
        "keywords": "Software Engineer",
        "location": "Remote",
        "limit": 5
    })
    assert response.status_code == 202
    data = response.json()
    assert "job_id" in data
```

### 11.4 E2E Tests

```javascript
// cypress/e2e/full-flow.cy.js
describe('Complete Job Application Flow', () => {
  beforeEach(() => {
    cy.login('test@example.com', 'password123')
  })

  it('uploads resume, finds matches, and starts application', () => {
    cy.visit('/resumes')
    cy.get('[data-testid="resume-upload"]').attachFile('sample_resume.pdf')
    cy.get('[data-testid="parse-button"]').click()
    cy.get('[data-testid="parse-success"]', { timeout: 30000 }).should('be.visible')

    cy.visit('/jobs')
    cy.get('[data-testid="search-keywords"]').type('Software Engineer')
    cy.get('[data-testid="search-location"]').type('Remote')
    cy.get('[data-testid="search-button"]').click()
    cy.get('[data-testid="job-card"]', { timeout: 60000 }).should('have.length.at.least', 1)

    cy.visit('/matches')
    cy.get('[data-testid="generate-matches"]').click()
    cy.get('[data-testid="match-card"]', { timeout: 30000 }).should('have.length.at.least', 1)

    cy.get('[data-testid="match-card"]').first().within(() => {
      cy.get('[data-testid="apply-button"]').click()
    })

    cy.url().should('include', '/applications/')
    cy.get('[data-testid="application-status"]').should('contain', 'queued')
  })
})
```

### 11.5 Load Testing

```python
# tests/load/locustfile.py
from locust import HttpUser, task, between

class JobCopilotUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        response = self.client.post("/api/v1/auth/login", json={
            "email": "loadtest@example.com",
            "password": "testpass123"
        })
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    @task(3)
    def get_matches(self):
        self.client.get("/api/v1/matches?limit=20", headers=self.headers)

    @task(2)
    def get_jobs(self):
        self.client.get("/api/v1/jobs?limit=50", headers=self.headers)

    @task(1)
    def upload_resume(self):
        with open("tests/fixtures/sample_resume.pdf", "rb") as f:
            self.client.post(
                "/api/v1/resumes/upload",
                headers=self.headers,
                files={"file": ("resume.pdf", f, "application/pdf")}
            )
```

Run: `locust -f tests/load/locustfile.py --host=http://localhost:8000`

---

## 12. Deployment Guide

### 12.1 Local Development

```bash
# Start all infrastructure
make start

# Run migrations
make migrate

# Seed data
make seed

# Start all services (use tmux or multiple terminals)
make start-auth &
make start-parser &
make start-scraper &
make start-matcher &
make start-resume &
make start-applier &
make start-workers &
make start-frontend &

# Or use Docker Compose for everything
docker-compose -f docker-compose.full.yml up -d
```

### 12.2 Staging Deployment

```bash
# Build Docker images
docker build -t jobcopilot/auth:latest -f services/auth/Dockerfile .
docker build -t jobcopilot/parser:latest -f services/parser/Dockerfile .
# ... repeat for all services

# Push to registry
docker push jobcopilot/auth:latest

# Deploy to staging K8s cluster
kubectl config use-context staging
helm upgrade --install jobcopilot ./helm-chart   --namespace staging   --values values-staging.yaml   --set image.tag=latest

# Verify
kubectl get pods -n staging
kubectl logs -f deployment/auth -n staging
```

### 12.3 Production Deployment

```bash
# 1. Tag release
git tag -a v1.0.0 -m "Production release v1.0.0"
git push origin v1.0.0

# 2. CI builds and pushes images with version tag
# GitHub Actions handles this automatically

# 3. Terraform plan
terraform -chdir=terraform/production plan

# 4. Terraform apply (after review)
terraform -chdir=terraform/production apply

# 5. Helm deploy with blue-green strategy
helm upgrade --install jobcopilot ./helm-chart   --namespace production   --values values-production.yaml   --set image.tag=v1.0.0   --wait   --timeout 10m

# 6. Verify rollout
kubectl rollout status deployment/auth -n production
kubectl rollout status deployment/parser -n production

# 7. Run smoke tests
python scripts/smoke_tests.py --env=production

# 8. Monitor for 1 hour before declaring success
# Grafana dashboards, error rates, latency

# 9. If issues detected, rollback
helm rollback jobcopilot 0 -n production
```

---

## 13. Monitoring & Observability

### 13.1 Metrics (Prometheus)

```yaml
# prometheus/rules/jobcopilot.yml
groups:
  - name: jobcopilot
    rules:
      - alert: HighErrorRate
        expr: |
          (
            sum(rate(http_requests_total{status=~"5.."}[5m]))
            /
            sum(rate(http_requests_total[5m]))
          ) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is above 5% for {{ $labels.service }}"

      - alert: HighLatency
        expr: |
          histogram_quantile(0.99, 
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
          ) > 2
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High latency detected"
          description: "P99 latency is above 2s for {{ $labels.service }}"

      - alert: ScraperSuccessRateLow
        expr: |
          (
            sum(rate(scraper_jobs_completed_total{status="success"}[1h]))
            /
            sum(rate(scraper_jobs_completed_total[1h]))
          ) < 0.8
        for: 30m
        labels:
          severity: warning
        annotations:
          summary: "Scraper success rate low"
          description: "Scraper success rate is below 80%"

      - alert: ApplierQueueDepthHigh
        expr: |
          celery_queue_length{queue="applier"} > 1000
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "Applier queue backing up"
          description: "{{ $value }} applications waiting to be processed"

      - alert: DatabaseConnectionsHigh
        expr: |
          pg_stat_activity_count / pg_settings_max_connections * 100 > 80
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Database connection pool near limit"
```

### 13.2 Logging (Structured JSON)

```python
# services/shared/logging.py
import structlog
import logging
import sys

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

def get_logger(name: str):
    return structlog.get_logger(name)

# Usage
logger = get_logger("services.parser")
logger.info(
    "resume_parsed",
    resume_id=str(resume_id),
    user_id=str(user_id),
    parsing_time_ms=elapsed_ms,
    confidence_score=confidence,
    skills_extracted=len(skills),
)
```

### 13.3 Distributed Tracing (Jaeger)

```python
# services/shared/tracing.py
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor

def setup_tracing(service_name: str):
    provider = TracerProvider()
    jaeger_exporter = JaegerExporter(
        agent_host_name="jaeger-agent",
        agent_port=6831,
    )
    processor = BatchSpanProcessor(jaeger_exporter)
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    FastAPIInstrumentor.instrument_app(app)
    SQLAlchemyInstrumentor().instrument()
    RedisInstrumentor().instrument()
```

### 13.4 Grafana Dashboard

Import dashboard JSON from `monitoring/grafana/dashboards/jobcopilot-overview.json`

Key panels:
- Request rate per service (QPS)
- Error rate per service (%)
- P50/P95/P99 latency per endpoint
- Active users (WebSocket connections)
- Scraper jobs per hour (success/failure)
- Applier queue depth
- Database connection pool usage
- Redis memory usage
- Kubernetes pod CPU/memory
- Billing: MRR, active subscriptions, churn rate

---

## 14. Security Checklist

### 14.1 Authentication & Authorization

- [ ] Argon2id password hashing (NOT bcrypt)
- [ ] JWT with RS256 (asymmetric keys)
- [ ] Access token: 15 minutes
- [ ] Refresh token: 7 days, single-use, stored hashed
- [ ] MFA (TOTP) support
- [ ] Rate limiting: 5 login attempts per 15 min per IP
- [ ] Account lockout after 10 failed attempts
- [ ] OAuth 2.0 + OpenID Connect for SSO
- [ ] SAML 2.0 for Enterprise (Phase 4)
- [ ] RBAC with resource-level permissions
- [ ] API key management for service-to-service auth

### 14.2 Data Protection

- [ ] TLS 1.3 everywhere (no TLS 1.0/1.1)
- [ ] HSTS headers
- [ ] AES-256-GCM encryption at rest (S3, RDS)
- [ ] Field-level encryption for PII (SSN, DOB)
- [ ] Encryption key rotation every 90 days
- [ ] Data retention policies (GDPR/CCPA)
- [ ] Right to erasure implementation
- [ ] Data portability (JSON export)

### 14.3 Application Security

- [ ] Input validation (Pydantic schemas)
- [ ] SQL injection prevention (SQLAlchemy ORM)
- [ ] XSS prevention (React auto-escaping, CSP headers)
- [ ] CSRF protection (Double-submit cookies)
- [ ] File upload validation (type, size, malware scan)
- [ ] SSRF prevention (URL whitelist for scraper)
- [ ] Dependency scanning (Snyk, Dependabot)
- [ ] Container scanning (Trivy)
- [ ] Secrets management (AWS Secrets Manager)
- [ ] Security headers (CSP, X-Frame-Options)

### 14.4 Compliance

- [ ] GDPR compliance (EU users)
- [ ] CCPA compliance (California users)
- [ ] SOC 2 Type II (Phase 4)
- [ ] ISO 27001 (Phase 4)
- [ ] Penetration testing (quarterly)
- [ ] Bug bounty program (HackerOne)
- [ ] Audit logs (7-year retention)
- [ ] Data processing agreements (DPA) with vendors

### 14.5 Infrastructure Security

- [ ] VPC isolation
- [ ] Security groups (least privilege)
- [ ] WAF rules (OWASP Top 10)
- [ ] DDoS protection (AWS Shield)
- [ ] Network segmentation (microservices)
- [ ] Pod security policies (Kubernetes)
- [ ] Image scanning before deployment
- [ ] Runtime threat detection (Falco)

---

## 15. Troubleshooting

### 15.1 Common Issues

#### Parser fails to extract text from PDF

```bash
# Check if PDF is image-based (scanned)
python -c "import pdfplumber; pdf=pdfplumber.open('resume.pdf'); print(len(pdf.pages[0].extract_text() or ''))"

# If 0 characters, it's image-based
# Solution: Use OCR (Tesseract) or ask user for text-based PDF
```

#### Scraper detected by job board

```bash
# Check browser fingerprint
python scripts/check_fingerprint.py

# Rotate user agents
# Enable residential proxies
# Increase delays between requests
# Use Playwright stealth plugins
```

#### Playwright browser crashes

```bash
# Reinstall browsers
playwright install --force chromium

# Check system dependencies
playwright install-deps chromium

# Increase memory limits
export PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-browsers
```

#### Database connection pool exhausted

```bash
# Check active connections
psql -c "SELECT count(*), state FROM pg_stat_activity GROUP BY state;"

# Increase pool size in SQLAlchemy
# Add connection pooling (PgBouncer)
# Check for connection leaks
```

#### Celery tasks not processing

```bash
# Check queue depth
redis-cli LLEN celery

# Check worker status
celery -A services.shared.celery_app inspect active

# Restart workers
celery multi restart worker1 -A services.shared.celery_app
```

### 15.2 Debug Mode

Enable debug logging:

```bash
export LOG_LEVEL=DEBUG
export PLAYWRIGHT_DEBUG=1
export SQLALCHEMY_ECHO=1
```

### 15.3 Support Contacts

| Issue Type | Contact | Response Time |
|-----------|---------|---------------|
| Production outage | pagerduty@jobcopilot.io | 15 minutes |
| Security incident | security@jobcopilot.io | 1 hour |
| General questions | support@jobcopilot.io | 24 hours |
| Feature requests | product@jobcopilot.io | 48 hours |

---

## Appendix A: Environment Variables

```bash
# Required
DATABASE_URL=postgresql://user:pass@host:5432/dbname
REDIS_URL=redis://host:6379/0
OPENAI_API_KEY=sk-...
JWT_SECRET_KEY=super-secret-rsa-key
ENCRYPTION_KEY=32-byte-aes-key

# Optional (with defaults)
LOG_LEVEL=INFO
ENVIRONMENT=development
DEBUG=false
CORS_ORIGINS=http://localhost:3000
MAX_UPLOAD_SIZE=10485760
SCRAPER_DELAY_MIN=2
SCRAPER_DELAY_MAX=5
MAX_APPLICATIONS_PER_DAY=15

# Phase 2+
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PUBLISHABLE_KEY=pk_test_...

# Phase 3+
ELASTICSEARCH_URL=http://localhost:9200
QDRANT_URL=http://localhost:6333
RABBITMQ_URL=amqp://jobcopilot:pass@localhost:5672/
S3_ENDPOINT=http://localhost:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
S3_BUCKET=jobcopilot-resumes

# Phase 4+
SAML_CERTIFICATE=...
SAML_PRIVATE_KEY=...
```

---

## Appendix B: Project Structure

```
job-copilot/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── cd-staging.yml
│       └── cd-production.yml
├── alembic/
│   ├── versions/
│   └── env.py
├── docker/
│   ├── Dockerfile.auth
│   ├── Dockerfile.parser
│   ├── Dockerfile.scraper
│   ├── Dockerfile.matcher
│   ├── Dockerfile.resume-builder
│   ├── Dockerfile.applier
│   └── Dockerfile.frontend
├── docs/
│   ├── api.md
│   ├── architecture.md
│   └── deployment.md
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── lib/
│   │   └── types/
│   ├── public/
│   └── package.json
├── helm-chart/
│   ├── templates/
│   ├── values.yaml
│   ├── values-staging.yaml
│   └── values-production.yaml
├── monitoring/
│   ├── grafana/
│   ├── prometheus/
│   └── jaeger/
├── scripts/
│   ├── seed_dev_data.py
│   ├── smoke_tests.py
│   └── migrate.sh
├── services/
│   ├── auth/
│   ├── parser/
│   ├── scraper/
│   ├── matcher/
│   ├── resume-builder/
│   ├── applier/
│   └── shared/
│       ├── celery_app.py
│       ├── logging.py
│       ├── tracing.py
│       └── models.py
├── terraform/
│   ├── modules/
│   ├── staging/
│   └── production/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   └── load/
├── .env.example
├── .gitignore
├── docker-compose.dev.yml
├── docker-compose.full.yml
├── Makefile
├── README.md
├── build.md
├── requirements.txt
├── requirements-dev.txt
└── pyproject.toml
```

---

**End of Build Guide**

For questions or issues, refer to the troubleshooting section or contact the development team.
