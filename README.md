# 🚀 ApplyPilot: Production-Grade AI Job Application Platform

[![CI/CD Pipeline](https://github.com/saiarjunkoyalkar756-sudo/ApplyPilot/actions/workflows/ci.yml/badge.svg)](https://github.com/saiarjunkoyalkar756-sudo/ApplyPilot/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**ApplyPilot** is a sophisticated, AI-driven job application automation platform built with a microservices architecture. It streamlines the entire job search lifecycle—from resume parsing and job discovery to tailored resume generation and automated browser-based applications.

---

## 🏗️ Architecture Overview

ApplyPilot is built for scale using a **Microservices Architecture**:

- **Auth Service:** Secure user registration, login, and profile management.
- **Parser Service:** AI-powered extraction of structured JSON data from PDF/DOCX resumes.
- **Scraper Service:** Distributed job board scraping (Indeed, LinkedIn, etc.) using Playwright.
- **Matcher Service:** Vector-based semantic matching to find the best job-fit scores.
- **Resume Builder:** Dynamic tailoring of resumes and cover letters using LLMs.
- **Applier Service:** Automated, human-in-the-loop application filling using Playwright cluster.

---

## ✨ Key Features

- **📄 AI Resume Parsing:** Converts raw resumes into structured data for better matching.
- **🔍 Intelligent Scraping:** stealth-optimized scraping of major job boards with automatic pagination.
- **💯 Semantic Matching:** Goes beyond keywords to find jobs that actually match your experience level and skills.
- **🛠️ Auto-Tailoring:** Automatically rewrites resume bullets and generates cover letters for every unique job description.
- **🚀 One-Click Apply:** Automates the filling of Greenhouse, Lever, and Workday forms.
- **📈 Pipeline Tracking:** A Kanban-style dashboard to manage your application statuses.
- **🛡️ Observability:** Integrated with OpenTelemetry and Jaeger for distributed tracing and Structlog for JSON logging.

---

## 🛠️ Technology Stack

### Backend (Python / FastAPI)
- **Framework:** FastAPI
- **Task Queue:** Celery + Redis
- **ORM:** SQLAlchemy 2.0 + Alembic
- **AI:** OpenAI GPT-4o / LangChain
- **Automation:** Playwright (Stealth Mode)
- **Observability:** OpenTelemetry, Jaeger, Structlog

### Frontend (Next.js)
- **Framework:** Next.js 14 (App Router)
- **Styling:** Tailwind CSS + Framer Motion
- **State Management:** Zustand + React Query
- **UI Components:** Lucide React

### Infrastructure
- **Containerization:** Docker & Docker Compose
- **Orchestration:** Kubernetes (Helm Charts provided)
- **Cloud (IaC):** Terraform (AWS VPC, EKS, RDS, S3)
- **CI/CD:** GitHub Actions

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js 20+
- Docker & Docker Compose
- OpenAI API Key

### Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/saiarjunkoyalkar756-sudo/ApplyPilot.git
   cd ApplyPilot
   ```

2. **Start Infrastructure (DB, Redis, etc.):**
   ```bash
   make start
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt -r requirements-dev.txt
   cd frontend && npm install && cd ..
   ```

4. **Run Migrations & Seed Data:**
   ```bash
   make migrate
   make seed
   ```

5. **Launch Services:**
   You can start services individually using the Makefile:
   ```bash
   make start-auth
   make start-parser
   # ...etc
   ```

---

## 📊 Database Schema

The platform uses a robust PostgreSQL schema managed via Alembic:
- `users`: Core user accounts and profiles.
- `resumes`: Versioned resume data and parsed JSON.
- `jobs`: Aggregated job listings from multiple sources.
- `matches`: Similarity scores between resumes and jobs.
- `applications`: Tracking for automated and manual applications.

---

## 🤝 Contributing

Contributions are welcome! Please read the `CONTRIBUTING.md` (coming soon) for details on our code of conduct and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Developed by [KOYALKAR SAHITHI](mailto:koyalkarsahithi956@gmail.com)**
