# InsightPilot — Decision Intelligence Platform

InsightPilot is an LLM-empowered automated data exploration and business intelligence system. It ingests spreadsheets, runs deterministic statistical profiling (Business Pulse, KPIs, recommendations), compiles grounded context, and offers an interactive AI Business Analyst chatbot powered by Gemini API.

---

## 🚀 Key Features
* **Universal Dataset Ingestion:** Fault-tolerant CSV and Excel uploading.
* **Deterministic Analytics Engine:** Calculates KPIs, trends, anomalies, and overall Business Pulse scores without model hallucinations.
* **Grounded AI Analyst:** Chat interface backed by live Gemini model reasoning using structured citations and validation safeguards.
* **Executive Reports Hub:** Downloadable, clean PDF briefs mapping business health.
* **Adaptive Dashboard:** Visual metrics rendering and workspace persistence.

---

## 🛠️ Tech Stack
* **Frontend:** React + Vite, Tailwind CSS, TypeScript, Lucide Icons
* **Backend:** FastAPI, SQLAlchemy, Alembic (Database Migrations), Uvicorn / Gunicorn
* **Database:** PostgreSQL
* **Model Integration:** Gemini Pro / Gemini Flash (`google-generativeai`)

---

## 💻 Local Development Setup

### 1. Prerequisites
* Python 3.10+
* Node.js 18+
* PostgreSQL 15+

### 2. Backend Installation & Boot
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   # On Windows:
   .\.venv\Scripts\Activate
   # On Unix/macOS:
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure the environment variables in `backend/.env`. (See [Environment Variables](#environment-variables) section).
5. Run migrations:
   ```bash
   alembic upgrade head
   ```
6. Start the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

### 3. Frontend Installation & Boot
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install node dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
4. Access the client interface at `http://localhost:5173`.

---

## 🐳 Docker Deployment Setup (Containerized)

InsightPilot is fully dockerized with a three-container architecture: PostgreSQL Database, FastAPI Backend, and Nginx serving React static assets while reverse proxying API calls.

### 1. Docker Build & Start Commands
From the project workspace root directory, run:
```bash
# Build and launch all services in background
docker compose up --build -d

# View service logs
docker compose logs -f

# Shut down and clear containers
docker compose down -v
```

### 2. Access Ports inside Docker
* **Frontend UI & API Proxy:** `http://localhost` (Port 80)
* **FastAPI Swagger Docs:** `http://localhost/docs` (Port 80 via Nginx proxy, or `http://localhost:8000/docs` directly)
* **PostgreSQL DB:** `localhost:5432`

---

## 🔑 Environment Variables

The backend loads configuration from `backend/.env`. Keep secrets out of repository commits.

| Variable Name | Purpose | Example / Default |
| :--- | :--- | :--- |
| `PROJECT_NAME` | Main platform name | `InsightPilot` |
| `POSTGRES_USER` | Database user account | `postgres` |
| `POSTGRES_PASSWORD` | Database user password | `mallu` |
| `POSTGRES_HOST` | Hostname (use `db` in Docker) | `localhost` |
| `POSTGRES_PORT` | PostgreSQL port | `5432` |
| `POSTGRES_DB` | Database schema name | `insightpilot` |
| `DATABASE_URL` | Complete DB connection string | `postgresql://postgres:mallu@localhost:5432/insightpilot` |
| `GEMINI_API_KEY` | Studio key credential | `AQ.Ab8RN6LlkeW...` |
| `GEMINI_MODEL` | Grounded model tag | `gemini-3.5-flash` |

---

## ☁️ AWS Deployment Steps (Production Readiness)

InsightPilot is built to be compliant with container platforms like **AWS App Runner**, **AWS ECS (Fargate)**, or **AWS Elastic Beanstalk**.

### Recommended Architecture: AWS ECS Fargate
1. **Push Container Images to Amazon ECR:**
   * Create two ECR repositories: `insightpilot-backend` and `insightpilot-frontend`.
   * Authenticate your local Docker client and push built images:
     ```bash
     docker tag insightpilot-backend:latest <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/insightpilot-backend:latest
     docker push <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/insightpilot-backend:latest
     ```
2. **Provision Amazon RDS PostgreSQL:**
   * Create a PostgreSQL database instance.
   * Set security groups to allow traffic from the ECS container security groups on port 5432.
3. **Configure AWS Systems Manager Parameter Store / Secrets Manager:**
   * Store `GEMINI_API_KEY` and connection strings (`DATABASE_URL`) securely.
4. **Deploy ECS Task Definitions:**
   * Configure backend task to run `alembic upgrade head` as an init container or task startup CMD.
   * Link the frontend container task to load environment variable `VITE_API_URL` pointing to the API load balancer DNS.

---

## 🔧 Troubleshooting
* **DB Connection Failure:** If backend fails to start inside Docker, ensure the PostgreSQL service healthcheck is running. Docker Compose holds the backend boot until `insightpilot-db` passes its `pg_isready` check.
* **Caret blinking cursor on text:** This behavior is disabled globally in static views via CSS (`caret-color: transparent`). Normal input inputs and textareas retain active cursors.
* **API Timeout issues:** Nginx is pre-configured with a `300s` proxy read timeout to prevent 504 errors on deep LLM text summaries.
