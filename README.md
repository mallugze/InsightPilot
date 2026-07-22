
# 🚀 InsightPilot – AI-Powered Decision Intelligence Platform

> **See Beyond the Numbers. Make Better Business Decisions with AI.**

InsightPilot is an AI-powered Decision Intelligence Platform that transforms spreadsheets into executive insights, business reports, and AI-driven recommendations within minutes.

Instead of spending hours building dashboards or manually analyzing data, InsightPilot acts as your **AI Business Analyst**—understanding your data, uncovering hidden opportunities, identifying risks, and helping organizations make confident, data-driven decisions.

---

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-4-38BDF8?style=for-the-badge&logo=tailwindcss&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google-Gemini_AI-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-Reverse_Proxy-009639?style=for-the-badge&logo=nginx&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-success?style=for-the-badge)

</p>

# 📸 Product Preview

## 🏠 Landing Page
![Landing Page](screenshots/landing-page.png)

## 📊 Dashboard
![Dashboard](screenshots/dashboard.png)

## 📂 Upload Dataset
![Upload Dataset](screenshots/upload.png)

## 🤖 AI Business Analyst
![AI Analyst](screenshots/AI-Analyst.png)

## 📈 Analysis History
![Analysis History](screenshots/analysis-history.png)

## 📄 Executive Reports
![Reports](screenshots/reports.png)

## ⚙️ Settings
![Settings](screenshots/settings.png)

# 💡 Why InsightPilot?

InsightPilot combines deterministic business analytics with Google's Gemini AI to transform raw spreadsheets into actionable business intelligence. Upload a dataset, explore insights, chat with an AI business analyst, and generate executive-ready reports—all from one platform.

# ✨ Key Features

- 📂 Smart Dataset Upload
- 📊 Automatic KPI Generation
- 🤖 AI Business Analyst
- 📈 Interactive Dashboard
- 📄 Executive Reports
- 📁 Workspace & Analysis History

# 🏗️ System Architecture

```mermaid
flowchart TD
U[User] --> FE[React + TypeScript + Tailwind]
FE --> API[FastAPI Backend]
API --> AN[Business Analysis Engine]
AN --> PD[Pandas + NumPy]
API --> AI[Google Gemini]
API --> DB[(PostgreSQL)]
FE --> NG[Nginx]
NG --> DC[Docker Compose]
API --> DC
DB --> DC
```

# 🛠️ Tech Stack

**Frontend:** React 19, TypeScript, Tailwind CSS, Vite

**Backend:** FastAPI, SQLAlchemy, Alembic, Pandas, NumPy, Uvicorn

**AI:** Google Gemini API

**Database:** PostgreSQL

**DevOps:** Docker, Docker Compose, Nginx

# 💻 Local Development

```bash
cd backend
python -m venv .venv
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

```bash
cd frontend
npm install
npm run dev
```



# 🐳 Docker

```bash
docker compose up --build -d
docker compose logs -f
docker compose down
```



# 🔑 Environment Variables

```env
DATABASE_URL=postgresql://your_username:your_password@db:5432/insightpilot
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

# ☁️ Deployment

Deploy with Docker to AWS ECS/Fargate, using Amazon RDS for PostgreSQL and Amazon ECR for container images.

# 👨‍💻 Developed By

**Mallikarjun**

AI & Machine Learning Engineer

IBM SkillsBuild Project

# ⭐ If you like this project, consider giving it a star!
