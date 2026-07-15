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

# Setup test DB
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

def test_semantic_profiles_generation():
    clean_temp_uploads()
    
    # --- DATASET 1: IRIS FLOWER (Biology / Scientific) ---
    iris_csv = (
        "sepal_length,sepal_width,petal_length,petal_width,species\n"
        "5.1,3.5,1.4,0.2,setosa\n"
        "4.9,3.0,1.4,0.2,setosa\n"
        "4.7,3.2,1.3,0.2,versicolor\n"
        "4.6,3.1,1.5,0.2,versicolor\n"
        "5.0,3.6,1.4,0.2,setosa\n"
    )
    res_upload = client.post(
        "/api/v1/upload",
        files={"file": ("iris.csv", io.BytesIO(iris_csv.encode("utf-8")), "text/csv")},
        headers={"X-Session-ID": "test-session-iris"}
    )
    assert res_upload.status_code == 201
    ds_id = res_upload.json()["dataset_id"]
    
    res_analyze = client.post(f"/api/v1/analyze/{ds_id}")
    assert res_analyze.status_code == 201
    profile = res_analyze.json()["semantic_profile"]
    print("IRIS FEATURES PROFILE:", profile["features"])
    print("IRIS RELATIONSHIPS:", profile["relationships"])
    print("IRIS ML READINESS:", profile["ml_readiness"])
    
    assert profile["domain"] == "Scientific"
    assert profile["subdomain"] == "Biology"
    assert profile["use_case"] == "Iris Classification"
    assert profile["intent"] == "Species Prediction"
    assert profile["entity"] == "Flower"
    assert profile["ml_readiness"]["classification"]["score"] > 50
    assert "flower" in profile["understanding_reasoning"].lower()
    assert any(viz["intent"] == "Comparison" for viz in profile["visualization_intent"])
    
    # Assert Workspace details
    assert "suggested_workspace_name" in profile
    assert profile["suggested_icon"] == "🌸"
    assert profile["color_theme"] == "pink"
    assert len(profile["dashboard_sections"]) > 0
    assert "Random Forest Classifier" in profile["suggested_models"]
    
    # Assert multi-level confidences
    assert "domain_confidence" in profile
    assert "subdomain_confidence" in profile
    assert "overall_confidence" in profile
    assert "quality" in profile
    
    # --- DATASET 2: TITANIC PASSENGERS (ML Benchmark) ---
    titanic_csv = (
        "passenger_id,survived,pclass,name,sex,age,fare\n"
        "1,0,3,Braund,male,22,7.25\n"
        "2,1,1,Cumings,female,38,71.28\n"
        "3,1,3,Heikkinen,female,26,7.92\n"
        "4,1,1,Futrelle,female,35,53.1\n"
        "5,0,3,Allen,male,35,8.05\n"
    )
    res_upload2 = client.post(
        "/api/v1/upload",
        files={"file": ("titanic.csv", io.BytesIO(titanic_csv.encode("utf-8")), "text/csv")},
        headers={"X-Session-ID": "test-session-titanic"}
    )
    assert res_upload2.status_code == 201
    ds_id2 = res_upload2.json()["dataset_id"]
    
    res_analyze2 = client.post(f"/api/v1/analyze/{ds_id2}")
    assert res_analyze2.status_code == 201
    profile2 = res_analyze2.json()["semantic_profile"]
    print("TITANIC FEATURES PROFILE:", profile2["features"])
    print("TITANIC RELATIONSHIPS:", profile2["relationships"])
    print("TITANIC ML READINESS:", profile2["ml_readiness"])
    
    assert profile2["domain"] == "Machine Learning"
    assert profile2["subdomain"] == "Classification Benchmark"
    assert profile2["use_case"] == "Titanic Survival"
    assert profile2["entity"] == "Passenger"
    assert profile2["ml_readiness"]["classification"]["score"] > 50
    assert "passenger" in profile2["understanding_reasoning"].lower()
    assert profile2["suggested_icon"] == "🚢"
    assert profile2["color_theme"] == "slate"

    # --- DATASET 3: REGULAR BUSINESS SALES ---
    sales_csv = (
        "transaction_id,date,revenue,cost,product_category\n"
        "1,2026-01-01,150.00,50.00,Electronics\n"
        "2,2026-01-02,200.00,80.00,Electronics\n"
        "3,2026-01-03,50.00,20.00,Clothing\n"
    )
    res_upload3 = client.post(
        "/api/v1/upload",
        files={"file": ("sales.csv", io.BytesIO(sales_csv.encode("utf-8")), "text/csv")},
        headers={"X-Session-ID": "test-session-sales"}
    )
    assert res_upload3.status_code == 201
    ds_id3 = res_upload3.json()["dataset_id"]
    
    res_analyze3 = client.post(f"/api/v1/analyze/{ds_id3}")
    assert res_analyze3.status_code == 201
    profile3 = res_analyze3.json()["semantic_profile"]
    kpi_suggs = profile3["kpi_suggestions"]
    print("SALES KPI SUGGESTIONS:", kpi_suggs)
    
    assert profile3["domain"] == "Business"
    assert profile3["subdomain"] == "Sales"
    assert profile3["use_case"] == "Revenue Analytics"
    assert profile3["entity"] == "Transaction"
    # Verify KPI aggregation suggestions
    kpi_suggs = profile3["kpi_suggestions"]
    assert any(k["aggregation_strategy"] == "SUM" and k["target_column"] == "revenue" for k in kpi_suggs)
    # Check explanation parameters are populated
    assert "selected_why" in kpi_suggs[0]
    
    print("All backend hierarchical semantic profiling tests PASSED successfully!")

if __name__ == "__main__":
    print("Running backend semantic analysis tests...")
    try:
        test_semantic_profiles_generation()
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
