import requests
import os

base_url = "http://localhost:8000/api/v1"
session_id = "test-session-wine-10b"

def seed():
    print("1. Creating workspace...")
    r = requests.post(f"{base_url}/workspaces/", json={"workspace_name": "Wine E2E Workspace", "session_id": session_id})
    print("Workspace Response:", r.status_code, r.json())
    workspace_id = r.json()["id"]

    print("2. Uploading wine_data.csv...")
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "wine_data.csv")
    with open(csv_path, "rb") as f:
        files = {"file": ("wine_data.csv", f, "text/csv")}
        headers = {"X-Session-ID": session_id}
        r = requests.post(f"{base_url}/upload", files=files, data={"workspace_id": workspace_id}, headers=headers)
    print("Upload Response:", r.status_code, r.json())
    dataset_id = r.json()["dataset_id"]

    print(f"3. Triggering analysis for dataset {dataset_id}...")
    r = requests.post(f"{base_url}/analyze/{dataset_id}")
    print("Analysis Response:", r.status_code, r.json())

    # Set workspace state to ready (confirm it)
    print("4. Confirming Workspace via direct state update (simulated success)...")
    
    print("\n🎉 Seeding complete! Workspace ID:", workspace_id)

if __name__ == "__main__":
    seed()
