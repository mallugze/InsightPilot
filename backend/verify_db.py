import sys
import logging
from sqlalchemy import create_engine, text
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("verify_db")

def verify_connection():
    db_url = settings.get_database_url()
    if db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+pg8000://", 1)
        
    logger.info(f"Attempting connection to database on: {settings.POSTGRES_HOST}:{settings.POSTGRES_PORT} (DB: {settings.POSTGRES_DB})")
    
    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("🎉 Database connectivity check SUCCESSFUL!")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Database connectivity check FAILED!")
        logger.error(f"Error Details: {str(e)}")
        logger.info("\nVerify that your PostgreSQL server is active and accessible with the credentials set inside 'backend/.env'.")
        # We exit with 1 to indicate failure but do not crash the script abnormally
        sys.exit(1)

if __name__ == "__main__":
    verify_connection()
