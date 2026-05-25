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
