import io
import os
import shutil
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database.session import Base, get_db

# Use local test SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Re-create database schemas on startup
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Apply the dependency override
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Helper function to remove test uploads
def clean_temp_uploads():
    temp_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "temp_uploads"))
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)
    if os.path.exists("./test.db"):
        try:
            os.remove("./test.db")
        except Exception:
            pass

def test_upload_missing_session_header():
    # Attempt upload without X-Session-ID
    file_content = b"col1,col2\n1,2\n3,4"
    files = {"file": ("test.csv", io.BytesIO(file_content), "text/csv")}
    response = client.post("/api/v1/upload", files=files)
    
    assert response.status_code == 400
    assert "X-Session-ID" in response.json()["error"]

def test_upload_invalid_extension():
    # Attempt upload of unsupported file type (.pdf)
    file_content = b"%PDF-1.4..."
    files = {"file": ("document.pdf", io.BytesIO(file_content), "application/pdf")}
    headers = {"X-Session-ID": "test-session-123"}
    response = client.post("/api/v1/upload", files=files, headers=headers)
    
    assert response.status_code == 400
    assert "Unsupported file format" in response.json()["error"]

def test_upload_empty_dataset():
    # Attempt upload of 0-byte file
    files = {"file": ("empty.csv", io.BytesIO(b""), "text/csv")}
    headers = {"X-Session-ID": "test-session-123"}
    response = client.post("/api/v1/upload", files=files, headers=headers)
    
    assert response.status_code == 400
    assert "empty" in response.json()["error"]

def test_upload_duplicate_headers():
    # Attempt upload with duplicate column headers
    file_content = b"sales_id,revenue,revenue\n1,100,100\n2,200,200"
    files = {"file": ("duplicates.csv", io.BytesIO(file_content), "text/csv")}
    headers = {"X-Session-ID": "test-session-123"}
    response = client.post("/api/v1/upload", files=files, headers=headers)
    
    assert response.status_code == 400
    assert "duplicate column headers" in response.json()["error"]

def test_upload_csv_success():
    # Valid Sales CSV Ingestion
    file_content = (
        b"transaction_id,sales_amount,customer_name,rate_percent,revenue_usd\n"
        b"1,150.50,Alice,0.15,$150.50\n"
        b"2,250.00,Bob,0.20,$250.00\n"
        b"3,350.25,Charlie,0.10,$350.25\n"
    )
    files = {"file": ("sales_data.csv", io.BytesIO(file_content), "text/csv")}
    headers = {"X-Session-ID": "test-session-123"}
    response = client.post("/api/v1/upload", files=files, headers=headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["rows"] == 3
    assert data["columns"] == 5
    assert data["dataset_type"] == "Sales"
    assert data["missing_values"] == 0
    assert data["duplicates"] == 0
    assert len(data["preview"]) == 3
    
    # Assert correct profiling outputs
    cols = data["column_metadata"]["columns"]
    assert len(cols) == 5
    
    # Assert column detections
    transaction_col = next(c for c in cols if c["name"] == "transaction_id")
    assert transaction_col["is_primary_key"] is True
    
    revenue_col = next(c for c in cols if c["name"] == "revenue_usd")
    assert revenue_col["is_currency"] is True

    rate_col = next(c for c in cols if c["name"] == "rate_percent")
    assert rate_col["is_percentage"] is True

def test_get_datasets_metadata():
    headers = {"X-Session-ID": "test-session-123"}
    response = client.get("/api/v1/datasets/1", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_upload_wine_headerless():
    # Simulate Wine CSV (Row 1 is metadata info, Row 2 onwards is actual data)
    file_content = (
        "3,2,class_0,class_1\n"
        "14.23,1.71\n"
        "13.2,1.78\n"
        "13.16,2.36\n"
    )
    files = {"file": ("wine_data.csv", io.BytesIO(file_content.encode("utf-8")), "text/csv")}
    headers = {"X-Session-ID": "test-session-wine"}
    response = client.post("/api/v1/upload", files=files, headers=headers)
    
    assert response.status_code == 201
    data = response.json()
    # It should detect no header, skip line 1, parse 3 rows of data, and generate safe placeholder column names
    assert data["rows"] == 3
    assert data["columns"] == 2
    
    cols = data["column_metadata"]["columns"]
    assert cols[0]["name"] == "numeric_1"
    assert cols[1]["name"] == "numeric_2"
    
    report = data["column_metadata"]["validation_report"]
    assert report["header_detected"] is False
    assert report["encoding"] == "utf-8"
    assert report["delimiter"] == ","
    assert report["validation_status"] == "success"

def test_upload_inconsistent_lengths_malformed():
    # Inconsistent column lengths (malformed CSV)
    file_content = (
        "col1,col2,col3\n"
        "1,2\n"
        "1,2,3,4,5\n"
    )
    files = {"file": ("malformed.csv", io.BytesIO(file_content.encode("utf-8")), "text/csv")}
    headers = {"X-Session-ID": "test-session-malformed"}
    response = client.post("/api/v1/upload", files=files, headers=headers)
    
    # It should return HTTP 400 validation_failed
    assert response.status_code == 400
    data = response.json()
    assert data["status"] == "validation_failed"
    assert len(data["details"]) > 0

if __name__ == "__main__":
    print("Running backend upload tests...")
    try:
        test_upload_missing_session_header()
        test_upload_invalid_extension()
        test_upload_empty_dataset()
        test_upload_duplicate_headers()
        test_upload_csv_success()
        test_get_datasets_metadata()
        test_upload_wine_headerless()
        test_upload_inconsistent_lengths_malformed()
        print("All backend unit tests PASSED successfully!")
    finally:
        clean_temp_uploads()
