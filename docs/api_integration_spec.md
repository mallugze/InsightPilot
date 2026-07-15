# API Integration Specification — FastAPI Backend Integration

This specification details the transition plan from localized frontend mock data states to a production FastAPI backend. It documents every backend endpoint, active data structures, headers, and target response payloads required for Sprint 5.

---

## 1. Global Authentication & Session Context

All requests sent to the backend require session tracking headers to isolate uploaded datasets, chat dialog streams, and workspaces under an anonymous browser context.

### Headers required:
- `X-Session-ID`: Unique browser session uuid (generated in localStorage and fetched via `getSessionId()`).

---

## 2. API Endpoint Registry

### A. Authentication Module
Backend Router Path: `/api/v1/auth`

#### 1. Register User Profile
- **Endpoint:** `POST /api/v1/auth/register`
- **Description:** Submits the user's Full Name, Email, and Company Name.
- **Request Payload:**
  ```json
  {
    "fullName": "Elena Rostova",
    "email": "elena@example.com",
    "companyName": "Insight Corp"
  }
  ```
- **Response Payload (200 OK):**
  ```json
  {
    "success": true,
    "userId": "usr_987654",
    "session_id": "session-uuid-xxxxx",
    "emailVerified": false,
    "message": "Verification code dispatched to email."
  }
  ```

#### 2. Confirm Email Code
- **Endpoint:** `POST /api/v1/auth/verify`
- **Description:** Submits 6-digit confirmation code.
- **Request Payload:**
  ```json
  {
    "code": "123456",
    "session_id": "session-uuid-xxxxx"
  }
  ```
- **Response Payload (200 OK):**
  ```json
  {
    "success": true,
    "isEmailVerified": true,
    "message": "Email address verified."
  }
  ```

---

### B. Dataset Upload Module
Backend Router Path: `/api/v1/datasets`

#### 1. Upload Spreadsheet File
- **Endpoint:** `POST /api/v1/datasets/upload`
- **Headers:** `X-Session-ID`
- **Request Payload:** Multipart Form Data (`file: File`)
- **Response Payload (201 Created):**
  ```json
  {
    "success": true,
    "datasetId": "ds_rev_q3",
    "fileName": "Sales_Q3_Final.csv",
    "fileSize": "2.4 MB",
    "format": "csv",
    "rowsCount": 1240,
    "colsCount": 12,
    "estimatedProcessingTimeSeconds": 6,
    "message": "File structured successfully."
  }
  ```

---

### C. AI Ingestion & Analysis Module
Backend Router Path: `/api/v1/analysis`

#### 1. Trigger AI Processing
- **Endpoint:** `POST /api/v1/analysis/run`
- **Headers:** `X-Session-ID`
- **Request Payload:**
  ```json
  {
    "datasetId": "ds_rev_q3"
  }
  ```
- **Response Payload (202 Accepted):**
  ```json
  {
    "success": true,
    "taskId": "task_ai_999",
    "message": "AI analysis started in background."
  }
  ```

#### 2. Fetch Pulse Scoring Details
- **Endpoint:** `GET /api/v1/analysis/pulse`
- **Headers:** `X-Session-ID`
- **Response Payload (200 OK):**
  ```json
  {
    "score": 87,
    "status": "healthy",
    "confidence": 92,
    "trendPercentage": 4.2
  }
  ```

#### 3. Fetch Core Business Insights
- **Endpoint:** `GET /api/v1/analysis/insights`
- **Headers:** `X-Session-ID`
- **Response Payload (200 OK):**
  ```json
  {
    "pulseScore": 87,
    "topCategory": "Electronics",
    "underperformingCategory": "Furniture",
    "primaryInsight": "Revenue grew by 14% this quarter, primarily driven by enterprise contract renewals. Mid-market CAC increased by 8%.",
    "recommendations": [
      {
        "id": "rec_1",
        "priority": "high",
        "title": "Improve customer retention campaign",
        "description": "Churn risk detected in mid-market segment. Proactive outreach recommended.",
        "impact": "High",
        "confidence": 94
      }
    ]
  }
  ```

---

### D. AI Assistant Chat Module
Backend Router Path: `/api/v1/chat`

#### 1. Ask Query
- **Endpoint:** `POST /api/v1/chat/message`
- **Headers:** `X-Session-ID`
- **Request Payload:**
  ```json
  {
    "message": "Compare this with last month",
    "sessionId": "session-uuid-xxxxx"
  }
  ```
- **Response Payload (200 OK):**
  ```json
  {
    "success": true,
    "message": {
      "id": "msg_987",
      "sender": "assistant",
      "content": "Q3 retail volume increased YoY by 12% following pricing shifts.",
      "timestamp": "10:14 PM"
    }
  }
  ```

---

### E. Reporting Module
Backend Router Path: `/api/v1/reports`

#### 1. Request Report Export
- **Endpoint:** `POST /api/v1/reports/export`
- **Headers:** `X-Session-ID`
- **Request Payload:**
  ```json
  {
    "datasetId": "ds_rev_q3",
    "format": "pdf"
  }
  ```
- **Response Payload (200 OK):**
  ```json
  {
    "success": true,
    "downloadUrl": "https://api.insightpilot.com/downloads/doc_123.pdf",
    "fileName": "Executive_Summary_Report.pdf",
    "sizeBytes": 1240000
  }
  ```

---

## 3. Mock Data Identification

The following UI modules are currently populated with static mocks and will be wired to these services in Sprint 5:
- **`WelcomePage` & `VerifyEmailPage`** ➔ Powered by `services/auth.ts`.
- **`UploadPage` File Drop** ➔ Powered by `services/upload.ts`.
- **`DashboardPage` Sparklines & Signal Metrics** ➔ Powered by `services/analysis.ts`.
- **`ReviewAnalysisPage` Summary Tables** ➔ Powered by `services/analysis.ts`.
- **`ProfilePage` Performance Stats** ➔ Managed by local session context + storage.
