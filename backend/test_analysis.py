import io
import os
import shutil
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database.session import Base, get_db
from app.models.dataset import Dataset
from app.models.analysis_result import AnalysisResult
from app.services.storage_service import TEMP_UPLOAD_DIR

# Configure test database
SQLALCHEMY_DATABASE_URL = "postgresql+pg8000://postgres:mallu@localhost:5432/insightpilot"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def clean_temp_uploads():
    if os.path.exists(TEMP_UPLOAD_DIR):
        shutil.rmtree(TEMP_UPLOAD_DIR)
    os.makedirs(TEMP_UPLOAD_DIR, exist_ok=True)

def test_analysis_pipeline_sales_success():
    clean_temp_uploads()
    
    # 1. Create a mock sales dataset in memory
    csv_content = (
        "transaction_id,customer_id,date,revenue,cost,product_category\n"
        "1,cust_101,2026-01-01,150.00,50.00,Electronics\n"
        "2,cust_102,2026-01-02,200.00,80.00,Electronics\n"
        "3,cust_103,2026-01-03,50.00,20.00,Clothing\n"
        "4,cust_101,2026-01-04,300.00,120.00,Electronics\n"
        "5,cust_104,2026-01-05,25.00,10.00,Clothing\n"
        "6,cust_102,2026-01-06,12.00,5.00,Clothing\n"
        "7,cust_105,2026-01-07,1500.00,400.00,Electronics\n"  # 1500 is a clear Z-score spike
        "8,cust_106,2026-01-08,180.00,70.00,Furniture\n"
        "9,cust_107,2026-01-09,220.00,90.00,Furniture\n"
        "10,cust_108,2026-01-10,190.00,75.00,Furniture\n"
    )
    
    # 2. Ingest the dataset via /api/v1/upload
    response_upload = client.post(
        "/api/v1/upload",
        files={"file": ("mock_sales.csv", io.BytesIO(csv_content.encode("utf-8")), "text/csv")},
        headers={"X-Session-ID": "test-session-789"}
    )
    assert response_upload.status_code == 201
    upload_data = response_upload.json()
    print("INGESTED COLUMN METADATA:", upload_data["column_metadata"])
    dataset_id = upload_data["dataset_id"]
    assert upload_data["dataset_type"] == "Sales"
    assert upload_data["rows"] == 10
    
    # 3. Trigger analysis via POST /api/v1/analyze/{dataset_id}
    response_analyze = client.post(f"/api/v1/analyze/{dataset_id}")
    assert response_analyze.status_code == 201
    res = response_analyze.json()
    
    # Verify Business Pulse Scorer
    assert "business_pulse" in res
    assert "health_label" in res
    assert "pulse_breakdown" in res
    assert "data_quality" in res["pulse_breakdown"]
    assert "completeness" in res["pulse_breakdown"]
    
    # Verify Dynamic KPIs
    kpis = res["kpis"]
    print("Calculated KPIs:", kpis)
    assert kpis["total_revenue"] == 2827.0
    assert kpis["total_orders"] == 10
    assert kpis["average_order_value"] == 282.7
    assert kpis["total_profit"] == 1907.0
    assert kpis["profit_margin"] == 67.5
    assert kpis["total_customers"] == 8
    
    # Verify Hero & Zero Groupings
    hero = res["hero"]
    print("Calculated Hero & Zero:", hero)
    assert hero["metric_name"] == "Revenue"
    assert hero["group_by_column"] == "Product Category"
    assert hero["hero_name"] == "Electronics"
    assert hero["zero_name"] == "Clothing"
    assert "top performer" in hero["reason"].lower()
    
    # Verify Trend Timeline Calculations
    trends = res["trends"]
    assert trends["has_trends"] is True
    assert trends["trend_direction"] in ["Upward", "Downward", "Stable"]
    assert len(trends["chart_data"]) == 10
    
    # Verify Anomalies (Z-score spike on row 7)
    anomalies = res["anomalies"]
    assert anomalies["anomalies_count"] > 0
    assert anomalies["anomalies"][0]["row_index"] == 7
    assert anomalies["anomalies"][0]["value"] == 1500.0
    assert anomalies["anomalies"][0]["type"] == "spike"
    
    # Verify Pearson Correlations
    correlations = res["correlations"]
    assert len(correlations["correlations"]) > 0
    first_corr = correlations["correlations"][0]
    assert first_corr["coefficient"] > 0.9  # Revenue and Cost correlate perfectly here
    
    # Verify Structured Rule Recommendations
    recs = res["recommendations"]
    assert len(recs) > 0
    assert "priority" in recs[0]
    assert "category" in recs[0]
    assert "recommendation" in recs[0]
    assert "reason" in recs[0]
    
    # Verify Deterministic Insights observations
    insights = res["insights"]
    assert len(insights) > 0
    assert any("sales" in ins.lower() or "revenue" in ins.lower() for ins in insights)

    # 4. Verify Caching GET /api/v1/analyze/{dataset_id}
    response_cached = client.get(f"/api/v1/analyze/{dataset_id}")
    assert response_cached.status_code == 200
    res_cached = response_cached.json()
    assert res_cached["id"] == res["id"]
    assert res_cached["business_pulse"] == res["business_pulse"]

def test_analysis_pipeline_wine_success():
    clean_temp_uploads()
    
    # 1. Read mock wine content
    with open("wine_data.csv", "r") as f:
        csv_content = f.read()
        
    # 2. Ingest via /api/v1/upload
    response_upload = client.post(
        "/api/v1/upload",
        files={"file": ("wine_data.csv", io.BytesIO(csv_content.encode("utf-8")), "text/csv")},
        headers={"X-Session-ID": "test-session-wine-analysis"}
    )
    assert response_upload.status_code == 201
    upload_data = response_upload.json()
    dataset_id = upload_data["dataset_id"]
    
    # 3. Trigger analysis via POST /api/v1/analyze/{dataset_id}
    response_analyze = client.post(f"/api/v1/analyze/{dataset_id}")
    assert response_analyze.status_code == 201
    res = response_analyze.json()
    
    # Assert successful analysis completion
    assert "business_pulse" in res
    assert "health_label" in res
    assert "semantic_profile" in res
    assert "dataset_domain" in res

if __name__ == "__main__":
    print("Running backend analysis tests...")
    try:
        test_analysis_pipeline_sales_success()
        test_analysis_pipeline_wine_success()
        print("All backend unit tests PASSED successfully!")
    finally:
        clean_temp_uploads()
        
        # Clean up database records created during test
        db = TestingSessionLocal()
        try:
            db.query(AnalysisResult).delete()
            db.query(Dataset).delete()
            db.commit()
        except:
            db.rollback()
        finally:
            db.close()
