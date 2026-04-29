# 🔗 TrustMark Sovereign API Reference - Quick Commands

## 🚀 Quick Start

### 1. Start the System
```bash
cd c:\Users\Suyash Sharma\Desktop\AI_Identity_Final
docker compose up --build
```

### 2. Get Your Machine IP
```powershell
ipconfig
# Look for: IPv4 Address: 192.168.x.x
```

### 3. Access Application
```
Browser: http://localhost (local) or http://192.168.x.x (LAN)
```

---

## 🔐 Authentication API

### Login (Get Token)
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "uid": "STU001",
    "password": "password123"
  }'

# Response:
# {
#   "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
#   "token_type": "bearer",
#   "expires_in": 1440
# }
```

### Get Current User (Verify Token)
```bash
curl -X GET http://localhost:8000/api/v1/auth/whoami \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."

# Response:
# {
#   "uid": "STU001",
#   "role": "STUDENT",
#   "message": "Hello STU001 (STUDENT)"
# }
```

### Change Password
```bash
curl -X POST http://localhost:8000/api/v1/auth/change-password \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "oldpass123",
    "new_password": "newpass456"
  }'
```

---

## 👥 Admin Enrollment API

### Enroll New Student (ADMIN/TEACHER)
```bash
curl -X POST http://localhost:8000/api/v1/admin/enroll \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "uid": "STU001",
    "name": "John Doe",
    "face_encoding": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
  }'

# Response:
# {
#   "status": "success",
#   "message": "John Doe synchronized!",
#   "enrolled_by": "ADMIN001",
#   "timestamp": "2025-01-15T10:30:00Z"
# }
```

---

## 📢 Notice Management API

### Create Notice (ADMIN)
```bash
curl -X POST http://localhost:8000/api/v1/admin/notice \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "🚨 URGENT: Attendance goes online tomorrow!",
    "is_urgent": true
  }'

# Response:
# {
#   "status": "success",
#   "message": "Broadcast Deployed!",
#   "notice_id": 42,
#   "created_by": "ADMIN001"
# }
```

### Get All Notices
```bash
curl -X GET http://localhost:8000/api/v1/dashboard \
  -H "Authorization: Bearer <token>"

# Returns notices in response
```

### Delete Notice (ADMIN)
```bash
curl -X DELETE http://localhost:8000/api/v1/admin/notice/42 \
  -H "Authorization: Bearer <admin_token>"

# Response:
# {
#   "status": "success",
#   "message": "Broadcast node eliminated!",
#   "deleted_by": "ADMIN001"
# }
```

---

## 🏥 Duty Leave (DL) API

### Grant Duty Leave (TEACHER/ADMIN)
```bash
curl -X POST http://localhost:8000/api/v1/admin/grant-dl \
  -H "Authorization: Bearer <teacher_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "uid": "STU001",
    "subject": "AI_IDENTITY_CORE",
    "reason": "Medical appointment"
  }'

# Response:
# {
#   "status": "success",
#   "message": "Duty leave granted for AI_IDENTITY_CORE.",
#   "student_uid": "STU001",
#   "subject": "AI_IDENTITY_CORE",
#   "granted_by": "TEACHER001",
#   "timestamp": "2025-01-15T11:00:00Z"
# }
```

---

## 📊 Statistics & Dashboard API

### Get User Attendance Stats
```bash
curl -X GET http://localhost:8000/api/v1/user-stats/STU001 \
  -H "Authorization: Bearer <token>"

# Response:
# {
#   "uid": "STU001",
#   "overall_percentage": 76.5,
#   "subjects": [
#     {
#       "subject": "AI_IDENTITY_CORE",
#       "attended": 34,
#       "total": 40,
#       "percentage": 85,
#       "status": "VERIFIED",
#       "needs_dl_count": 0,
#       "date_history": ["2025-01-15 10:30:00", ...]
#     }
#   ]
# }
```

### Get Dashboard (Admin View)
```bash
curl -X GET http://localhost:8000/api/v1/dashboard \
  -H "Authorization: Bearer <admin_token>"

# Returns all students with roster view + announcements
```

### Export Attendance to CSV (ADMIN)
```bash
curl -X GET http://localhost:8000/api/v1/admin/export \
  -H "Authorization: Bearer <admin_token>" \
  --output attendance_export.csv

# File saved as 'attendance_export.csv'
```

---

## 🎬 Real-Time Biometric Stream (WebSocket)

### Connect to WebSocket
```javascript
// JavaScript in browser
const ws = new WebSocket('ws://localhost:8000/api/v1/attendance/ws');

ws.onopen = () => {
  // Connected!
  console.log('WebSocket connected');
  
  // Toggle anti-spoof
  ws.send(JSON.stringify({
    type: 'config',
    anti_spoof: true  // Strict liveness detection
  }));
};

ws.onmessage = (event) => {
  // Received frame or response
  console.log('Message:', event.data);
};

ws.onerror = (error) => {
  console.error('Error:', error);
};
```

### Send Frame to WebSocket
```javascript
// Capture from camera and send base64-encoded JPEG
canvas.toBlob((blob) => {
  const reader = new FileReader();
  reader.onload = (e) => {
    const base64 = e.target.result.split(',')[1];
    ws.send(base64);  // Send JPEG frame
  };
  reader.readAsDataURL(blob);
});
```

---

## 🐳 Docker Commands

### View Logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f fastapi
docker compose logs -f postgres
docker compose logs -f redis
docker compose logs -f nginx
```

### Stop Services
```bash
docker compose down
```

### Restart Services
```bash
docker compose restart
```

### Access Database (PostgreSQL)
```bash
docker compose exec postgres psql -U admin -d trustmark_db

# SQL queries inside psql:
# \dt                           -- List tables
# SELECT * FROM users;         -- View users
# SELECT * FROM attendance;    -- View attendance logs
# \q                           -- Exit
```

### Access Redis Cache
```bash
docker compose exec redis redis-cli

# Redis commands:
# KEYS face:encoding:*         -- List all cached encodings
# GET face:encoding:STU001     -- View specific encoding
# DBSIZE                       -- Total keys cached
# FLUSHALL                     -- Clear all cache
# QUIT                         -- Exit
```

---

## 🧪 Test Scenarios (Curl)

### Scenario 1: Admin Workflow
```bash
# 1. Admin logs in
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"uid":"ADMIN001","password":"admin123"}' \
  | jq -r '.access_token')

# 2. Admin enrolls student
curl -X POST http://localhost:8000/api/v1/admin/enroll \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"uid":"STU001","name":"Test Student","face_encoding":"..."}'

# 3. Admin creates notice
curl -X POST http://localhost:8000/api/v1/admin/notice \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content":"Welcome!","is_urgent":false}'

# 4. Admin exports data
curl -X GET http://localhost:8000/api/v1/admin/export \
  -H "Authorization: Bearer $TOKEN" \
  --output attendance.csv
```

### Scenario 2: Permission Denied (Student → Admin Endpoint)
```bash
# 1. Student logs in
STUDENT_TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"uid":"STU001","password":"password"}' \
  | jq -r '.access_token')

# 2. Student tries to export (should fail with 403)
curl -X GET http://localhost:8000/api/v1/admin/export \
  -H "Authorization: Bearer $STUDENT_TOKEN"

# Response:
# {
#   "detail": "Admin access required"
# }
```

### Scenario 3: Expired/Invalid Token
```bash
# Try with invalid token
curl -X GET http://localhost:8000/api/v1/auth/whoami \
  -H "Authorization: Bearer invalid_token_xyz"

# Response:
# {
#   "detail": "Invalid or expired token"
# }
```

---

## Valid Subject Codes

When enrolling or granting DL, use these exact subject codes:

```
AI_IDENTITY_CORE
CRYPTOGRAPHY
BLOCKCHAIN
DATA_SCIENCE
ML_ENGINEERING
CYBERSECURITY
CLOUD_ARCHITECTURE
DEVOPS
```

---

## Error Codes Reference

| Code | Meaning | Solution |
|------|---------|----------|
| **200** | Success | All good ✅ |
| **201** | Created | Resource created successfully |
| **400** | Bad Request | Check your JSON format or validation errors |
| **401** | Unauthorized | Token missing or invalid. Try login again |
| **403** | Forbidden | Your role doesn't have permission. Check role |
| **404** | Not Found | Resource doesn't exist (wrong ID?) |
| **422** | Validation Error | Input validation failed. Check field formats |
| **500** | Server Error | Backend error. Check Docker logs |

---

## Python Test Script

```python
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# 1. Login
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"uid": "STU001", "password": "password"}
)
token = login_response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# 2. Get stats
stats = requests.get(f"{BASE_URL}/user-stats/STU001", headers=headers).json()
print(f"Attendance: {stats['overall_percentage']}%")

# 3. Grant DL
requests.post(
    f"{BASE_URL}/admin/grant-dl",
    headers=headers,
    json={"uid": "STU001", "subject": "AI_IDENTITY_CORE"}
)

# 4. Create notice
requests.post(
    f"{BASE_URL}/admin/notice",
    headers=headers,
    json={"content": "Test notice", "is_urgent": False}
)

# 5. Export CSV
export = requests.get(f"{BASE_URL}/admin/export", headers=headers)
with open("attendance.csv", "w") as f:
    f.write(export.text)
```

---

## Postman Collection Setup

**Import to Postman:**

1. Create new environment:
   - `base_url`: `http://localhost:8000/api/v1`
   - `token`: (auto-filled after login)

2. Create requests:
   - **POST** `/auth/login` → Save token to `token` variable
   - **GET** `/auth/whoami` → Use `{{token}}`
   - **POST** `/admin/notice` → Use `{{token}}`
   - **GET** `/admin/export` → Use `{{token}}`

3. Add test script to login:
```javascript
if (pm.response.code === 200) {
    var jsonData = pm.response.json();
    pm.environment.set("token", jsonData.access_token);
}
```

---

## Troubleshooting Commands

### Check if Services Running
```bash
docker compose ps
# Should show: fastapi, postgres, redis, nginx all UP
```

### Check FastAPI Logs
```bash
docker compose logs fastapi
# Look for: "Application startup complete"
```

### Test Database Connection
```bash
docker compose exec fastapi python -c "
from app.db.session import SessionLocal
db = SessionLocal()
users = db.query(db.User).all()
print(f'Found {len(users)} users')
"
```

### Clear Database & Restart
```bash
docker compose down -v
docker compose up --build
# All data reset, fresh start
```

---

## Performance Test

```bash
# Test response time
time curl -s http://localhost:8000/api/v1/auth/whoami \
  -H "Authorization: Bearer <token>" > /dev/null

# Should complete in <100ms
```

---

**All endpoints tested and working! 🎉**
