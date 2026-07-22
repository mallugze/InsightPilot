import logging
from fastapi import FastAPI, Depends, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging_config import setup_logging
from app.api.v1.api import api_router
from app.database.session import get_db

# Initialize JSON Structured Logging
setup_logging()
logger = logging.getLogger("main")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="InsightPilot Decision Intelligence Platform API Backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Fix 1: Allow Vercel origins and production domains alongside local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows local dev and any Vercel deployment domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.exceptions import DatasetValidationError

# Centralized Exception Handlers
@app.exception_handler(DatasetValidationError)
async def dataset_validation_error_handler(request: Request, exc: DatasetValidationError):
    logger.error(f"Dataset validation error: {exc.reason} - {exc.details}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "status": "validation_failed",
            "reason": exc.reason,
            "details": exc.details,
            "success": False,
            "error": f"{exc.reason}: {', '.join(exc.details)}"
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"HTTP exception: status_code={exc.status_code} detail={exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": exc.detail}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error occurred: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"success": False, "error": "Request validation failed", "details": exc.errors()}
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("An unhandled exception occurred in the server")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"success": False, "error": "Internal server error"}
    )

# Base routes
@app.get("/", include_in_schema=False)
def index_redirect():
    """
    Redirects root index to automatic Swagger API Documentation.
    """
    return RedirectResponse(url="/docs")

@app.get("/health", tags=["health"])
@app.get("/api/health", tags=["health"])
def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint reporting API server status and verifying database connectivity.
    """
    db_status = "disconnected"
    try:
        # Verify db connectivity
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        db_status = f"error: {str(e)}"
        
    return {
        "status": "healthy",
        "database": db_status
    }

# Register Sub-API routes under standard v1 prefix (/api/v1)
app.include_router(api_router, prefix=settings.API_V1_STR)

# Fix 2: Alias router under /api prefix for Vercel rewrite compatibility
if settings.API_V1_STR.startswith("/api"):
    # Also register without leading /api if Vercel strips it out
    alt_prefix = settings.API_V1_STR.replace("/api", "", 1)
    if alt_prefix:
        app.include_router(api_router, prefix=alt_prefix)