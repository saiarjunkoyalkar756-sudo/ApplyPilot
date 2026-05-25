#!/bin/bash
set -e

echo "1. Initializing Alembic..."
alembic init alembic

echo "2. Configuring Alembic to use the project models and Postgres..."
sed -i 's/sqlalchemy.url = driver:\/\/user:pass@localhost\/dbname/sqlalchemy.url = postgresql:\/\/jobcopilot:devpassword@localhost:5432\/jobcopilot_dev/' alembic.ini
sed -i '/target_metadata = None/c\import sys\nimport os\nsys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))\nfrom services.shared.models import Base\ntarget_metadata = Base.metadata' alembic/env.py

echo "3. Creating Next.js Frontend Framework..."
# Since frontend directory exists, we temporarily remove it to let create-next-app run cleanly
rm -rf frontend
npx create-next-app@14 frontend --ts --tailwind --eslint --app --src-dir --import-alias "@/*" --use-npm --yes
cd frontend

echo "4. Installing essential frontend dependencies..."
npm install lucide-react @radix-ui/react-dialog @radix-ui/react-slot class-variance-authority clsx tailwind-merge framer-motion zustand @tanstack/react-query axios react-hook-form @hookform/resolvers zod react-hot-toast date-fns recharts

echo "Project Architecture Built Successfully!"
