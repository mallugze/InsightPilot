from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Automatically translate standard postgresql:// schema to postgresql+pg8000:// for the pg8000 driver
db_url = settings.get_database_url()
if db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+pg8000://", 1)
# Handle empty fallback for sqlite during migration tests if required, but default to postgresql+pg8000
if not db_url:
    db_url = "postgresql+pg8000://postgres:postgres@localhost:5432/insightpilot"

engine = create_engine(
    db_url,
    # pg8000 does not need specialized thread flags
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
