╔════════════════════════════════════════════════════════════════════════════════╗
║                   🗺️  COMPLETE FEATURE LOCATION MAP                            ║
║         TrustMark Sovereign v25.0 - All Features & Where to Find Them           ║
╚════════════════════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════════════════════
🎯 QUICK ACCESS GUIDE
═══════════════════════════════════════════════════════════════════════════════════

FEATURE                  ENDPOINT                    ROLE REQUIRED    STATUS
─────────────────────────────────────────────────────────────────────────────────
📊 Analytics            POST /api/v1/admin/analytics      ADMIN          ✅ Line 25-42
👤 Enroll Student       POST /api/v1/admin/enroll         TEACHER+       ✅ Line 47-86
📢 BROADCAST NOTICE     POST /api/v1/admin/notice         ADMIN          ✅ Line 90-103
🏥 Duty Leave Grant     POST /api/v1/admin/grant-dl       TEACHER+       ✅ Line 103-122
📤 Export Data          GET  /api/v1/admin/export         ADMIN          ✅ Line 124-220
🎥 Real-time Biometric  WS   /api/v1/attendance/ws        ALL USERS      ✅ Line 16+
📋 Attendance History   GET  /api/v1/attendance/history   ALL USERS      ✅ Line 146+
📈 Attendance Summary   GET  /api/v1/attendance/summary   ADMIN          ✅ Line 194+
🚨 Duplicate Detection  GET  /api/v1/attendance/duplicates ADMIN         ✅ Line 233+
🔑 Login               POST /api/v1/auth/login            ALL            ✅ Line 18+
🚪 Logout              GET  /api/v1/auth/logout           ALL            ✅ Line 98+
👁️  Who Am I            GET  /api/v1/auth/whoami           ALL            ✅ Line 105+
🔐 Change Password     POST /api/v1/auth/change-password  ALL            ✅ Line 110+

═══════════════════════════════════════════════════════════════════════════════════
📢 BROADCAST FEATURE (NOTICE SYSTEM) - DETAILED LOCATION
═══════════════════════════════════════════════════════════════════════════════════

File: backend/app/api/v1/endpoints/admin.py
Location: Lines 90-103
Status: ✅ ACTIVE & WORKING

Code:
┌─────────────────────────────────────────────────────────────────────────────┐
│ @router.post("/notice")                                                     │
│ async def create_notice(                                                    │
│     data: NoticeCreate,                                                    │
│     db: Session = Depends(get_db),                                         │
│     current_user: TokenData = Depends(auth.require_admin)                 │
│ ):                                                                          │
│     new_notice = Notice(                                                   │
│         content=data.content,                                              │
│         is_urgent=data.is_urgent,                                          │
│         created_at=datetime.now()                                          │
│     )                                                                        │
│     db.add(new_notice)                                                     │
│     db.add(Activity(                                                       │
│         action=f"📢 BROADCAST: {data.content[:20]}...",                  │
│         user_id=current_user.uid                                          │
│     ))                                                                      │
│     db.commit()                                                             │
│     return {"status": "success", "message": "Signal Deployed"}            │
└─────────────────────────────────────────────────────────────────────────────┘

How to Use:
1. Admin logs in (role: ADMIN required)
2. Send POST request to /api/v1/admin/notice
3. Body: {"content": "Your message", "is_urgent": true/false}
4. Returns: {"status": "success", "message": "Signal Deployed"}
5. Notice saved to Notice table
6. Action logged to Activity audit trail

Database Tables Affected:
├─ Notice (new_notice saved)
└─ Activity (audit trail logged)

═══════════════════════════════════════════════════════════════════════════════════
📊 ANALYTICS FEATURE - DETAILED LOCATION
═══════════════════════════════════════════════════════════════════════════════════

File: backend/app/api/v1/endpoints/admin.py
Location: Lines 25-42
Status: ✅ ACTIVE & WORKING

Code:
┌─────────────────────────────────────────────────────────────────────────────┐
│ @router.get("/analytics")                                                   │
│ async def get_analytics(                                                   │
│     db: Session = Depends(get_db),                                         │
│     current_user: TokenData = Depends(auth.require_admin)                 │
│ ):                                                                          │
│     total_users = db.query(User).count()                                  │
│     total_notices = db.query(Notice).count()                              │
│                                                                             │
│     today_start = datetime.combine(datetime.now().date(), time.min)       │
│     today_attendance = db.query(Attendance)                               │
│         .filter(Attendance.timestamp >= today_start).count()              │
│                                                                             │
│     recent_activities = db.query(Activity)                                │
│         .order_by(Activity.id.desc()).limit(8).all()                      │
│                                                                             │
│     return {                                                               │
│         "users": total_users,                                              │
│         "notices": total_notices,                                          │
│         "today_records": today_attendance,                                 │
│         "recent": [...]                                                    │
│     }                                                                       │
└─────────────────────────────────────────────────────────────────────────────┘

Returns:
{
  "users": 25,
  "notices": 12,
  "today_records": 89,
  "recent": [
    {"id": 1, "action": "AUTH_SUCCESS", "user": "25BAI70757"},
    {"id": 2, "action": "BROADCAST: Important notice...", "user": "ADMIN"}
  ]
}

═══════════════════════════════════════════════════════════════════════════════════
👤 ENROLLMENT FEATURE - DETAILED LOCATION
═══════════════════════════════════════════════════════════════════════════════════

File: backend/app/api/v1/endpoints/admin.py
Location: Lines 47-86
Status: ✅ ACTIVE & WORKING
Role Required: TEACHER/ADMIN

Features:
├─ UID validation (auto uppercase)
├─ Face encoding capture
├─ Neural capture guard (validates face detected)
├─ Database merge/insert
├─ AI memory reload (dynamic update)
└─ Face recognition integration

Input: {uid, name, face_encoding}
Output: {"status": "success"}

Database Tables Affected:
├─ User (new student saved)
└─ Activity (audit trail logged)

═══════════════════════════════════════════════════════════════════════════════════
🏥 DUTY LEAVE (DL) FEATURE - DETAILED LOCATION
═══════════════════════════════════════════════════════════════════════════════════

File: backend/app/api/v1/endpoints/admin.py
Location: Lines 103-122
Status: ✅ ACTIVE & WORKING
Role Required: TEACHER/ADMIN

Features:
├─ CU semester lock (Jan-May validation)
├─ UID lookup and validation
├─ Subject validation
├─ Reason field (optional)
├─ Attendance status marked as "DUTY_LEAVE"
└─ Audit logging

Input: {uid, subject, reason}
Output: {"status": "success", "message": "Duty Leave Logged in Matrix"}

Database Tables Affected:
├─ Attendance (DL record created)
└─ Activity (audit trail logged)

═══════════════════════════════════════════════════════════════════════════════════
📤 EXPORT FEATURE - DETAILED LOCATION
═══════════════════════════════════════════════════════════════════════════════════

File: backend/app/api/v1/endpoints/admin.py
Location: Lines 124-220
Status: ✅ ACTIVE & WORKING
Role Required: ADMIN

Features:
├─ CSV generation
├─ All attendance records exported
├─ Column headers: uid, name, subject, status, timestamp
├─ File streaming
├─ Filename: attendance_export_{timestamp}.csv

Data Included:
├─ UID
├─ Student Name
├─ Subject
├─ Status (VERIFIED, DUPLICATE, DUTY_LEAVE)
└─ Timestamp

═══════════════════════════════════════════════════════════════════════════════════
🎥 BIOMETRIC REAL-TIME FEATURE - DETAILED LOCATION
═══════════════════════════════════════════════════════════════════════════════════

File: backend/app/api/v1/endpoints/attendance.py
Location: Lines 16+
Status: ✅ ACTIVE & WORKING
Type: WebSocket (Real-time streaming)

Features:
├─ Video frame capture
├─ Real-time face recognition
├─ 128D face embedding matching
├─ Duplicate detection
├─ Anti-spoof (liveness check)
├─ Live roster updates
└─ Performance: 4 FPS (250ms intervals)

Connection:
WS /api/v1/attendance/ws

Process:
1. Client connects via WebSocket
2. Sends video frames
3. Backend:
   - Detects face with face_recognition
   - Extracts 128D embedding
   - Compares with enrolled faces
   - Returns match (uid) or None
4. Client receives response
5. If matched → marks attendance
6. Updates UI roster in real-time

═══════════════════════════════════════════════════════════════════════════════════
📋 ATTENDANCE HISTORY - DETAILED LOCATION
═══════════════════════════════════════════════════════════════════════════════════

File: backend/app/api/v1/endpoints/attendance.py
Location: Lines 146-157
Status: ✅ ACTIVE & WORKING

Endpoint: GET /api/v1/attendance/history
Query Parameters:
├─ skip: Number of records to skip (default: 0)
├─ limit: Number of records to return (default: 10, max: 100)

Returns: Array of attendance records with:
├─ uid
├─ name
├─ subject
├─ timestamp
├─ status (VERIFIED, DUPLICATE, DUTY_LEAVE)
└─ face_match_score

═══════════════════════════════════════════════════════════════════════════════════
📈 ATTENDANCE SUMMARY - DETAILED LOCATION
═══════════════════════════════════════════════════════════════════════════════════

File: backend/app/api/v1/endpoints/attendance.py
Location: Lines 194-231
Status: ✅ ACTIVE & WORKING
Role Required: ADMIN

Endpoint: GET /api/v1/attendance/summary

Returns: Summary statistics including:
├─ Total attendance for each student
├─ Subject-wise breakdown
├─ Percentage calculations
├─ Status distribution
└─ Trend analysis

═══════════════════════════════════════════════════════════════════════════════════
🚨 DUPLICATE DETECTION - DETAILED LOCATION
═══════════════════════════════════════════════════════════════════════════════════

File: backend/app/api/v1/endpoints/attendance.py
Location: Lines 233-246
Status: ✅ ACTIVE & WORKING
File: backend/app/services/duplicate_detection.py

Features:
├─ Detects same person marking attendance twice
├─ Configurable time window
├─ Blocks duplicate marks in same session
├─ Alerts on duplicate attempt
└─ Reset capability for admin

Endpoint: GET /api/v1/attendance/duplicates
- Lists all duplicate attempts detected

Endpoint: POST /api/v1/attendance/reset-duplicate/{uid}/{subject}
- Admin reset duplicate block (role: ADMIN)

═══════════════════════════════════════════════════════════════════════════════════
🔑 AUTHENTICATION FEATURES - DETAILED LOCATIONS
═══════════════════════════════════════════════════════════════════════════════════

1️⃣ LOGIN ENDPOINT
   File: backend/app/api/v1/endpoints/auth.py (Lines 18-55)
   Endpoint: POST /api/v1/auth/login
   Features:
   ├─ UID + Password authentication
   ├─ Bcrypt password verification
   ├─ JWT token creation (1440 min expiry)
   ├─ HttpOnly cookie setting
   ├─ Audit logging
   └─ Redirect to dashboard

2️⃣ LOGOUT ENDPOINT
   File: backend/app/api/v1/endpoints/auth.py (Lines 98-103)
   Endpoint: GET /api/v1/auth/logout
   Features:
   ├─ Session termination
   ├─ Token invalidation
   └─ Clear cookies

3️⃣ WHO AM I ENDPOINT
   File: backend/app/api/v1/endpoints/auth.py (Lines 105-109)
   Endpoint: GET /api/v1/auth/whoami
   Returns: Current logged-in user info
   ├─ uid
   └─ role

4️⃣ CHANGE PASSWORD ENDPOINT
   File: backend/app/api/v1/endpoints/auth.py (Lines 110-122)
   Endpoint: POST /api/v1/auth/change-password
   Features:
   ├─ Current password verification
   ├─ New password hashing (Bcrypt)
   ├─ Database update
   └─ Audit logging

═══════════════════════════════════════════════════════════════════════════════════
🎯 FRONTEND ACCESS POINTS
═══════════════════════════════════════════════════════════════════════════════════

Dashboard: frontend/templates/index.html
├─ Shows: Video feed, real-time roster, registry count
├─ Features:
│  ├─ "ENROLL IDENTITY" button → Admin enrollment modal
│  ├─ "EXPORT LOGS" button → Triggers CSV download
│  ├─ Video feed → Real-time biometric stream
│  └─ User display → Current user info
└─ Status: ✅ GLASS MORPHISM DESIGN (450+ lines)

Admin Dashboard: frontend/templates/dashboard.html
├─ Analytics display
├─ Admin controls
└─ Status: ✅ AVAILABLE

Login Page: frontend/templates/login.html
├─ UID field
├─ Password field
└─ Status: ✅ AVAILABLE

═══════════════════════════════════════════════════════════════════════════════════
🔗 FEATURE DEPENDENCY DIAGRAM
═══════════════════════════════════════════════════════════════════════════════════

                          ┌─────────────────────────┐
                          │   USER LOGIN            │
                          │ /api/v1/auth/login      │
                          └────────────┬────────────┘
                                       │
                    ┌──────────────────┼──────────────────┐
                    │                  │                  │
              ┌─────▼──────┐     ┌────▼────┐      ┌────▼────────┐
              │ STUDENT     │     │ TEACHER │      │ ADMIN       │
              │ (View only) │     │ (DL, RL)│      │ (All admin) │
              └─────┬──────┘     └────┬────┘      └────┬────────┘
                    │                  │                  │
        ┌───────────┘                  │                  │
        │                              │                  │
   ┌────▼──────┐         ┌─────────────▼────┐    ┌──────▼────────┐
   │ Attendance│         │    Enrollment    │    │  Broadcast    │
   │ via WS    │         │ /admin/enroll    │    │  /admin/notice│
   │ WebSocket │         │ Neural Guard ✓   │    │               │
   │           │         │ AI Reload ✓      │    │ Export CSV ✓  │
   │ Face Match│         │                  │    │  Analytics ✓  │
   │ Recording │         │ Grant DL         │    │  Duplicates ✓ │
   └────┬──────┘         └────┬─────────────┘    └──────┬────────┘
        │                      │                        │
        │  ┌───────────────────┘                        │
        │  │                                            │
   ┌────▼──▼────────────────────────────────────┐      │
   │       DATABASE (PostgreSQL)                │      │
   ├──────────────────────────────────────────┤      │
   │ • User (uid, name, password, role)        │      │
   │ • Attendance (uid, subject, status)       │      │
   │ • Notice (content, is_urgent, date)───────┼──────┘
   │ • Activity (action, user_id, timestamp)   │
   │ • DutyLeave (uid, subject, reason)        │
   └────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════════
🗂️ FILE STRUCTURE BREAKDOWN
═══════════════════════════════════════════════════════════════════════════════════

backend/app/api/v1/endpoints/
├─ admin.py
│  ├─ Analytics (Line 25-42)
│  ├─ Enrollment (Line 47-86)
│  ├─ BROADCAST/Notice (Line 90-103) ⭐
│  ├─ DL Provisioning (Line 103-122)
│  └─ CSV Export (Line 124-220)
│
├─ auth.py
│  ├─ Login (Line 18-55)
│  ├─ Dependencies (auth.require_admin, auth.require_teacher_admin)
│  ├─ Logout (Line 98-103)
│  ├─ Whoami (Line 105-109)
│  └─ Change Password (Line 110-122)
│
└─ attendance.py
   ├─ WebSocket Biometric (Line 16+)
   ├─ Attendance History (Line 146-157)
   ├─ Summary (Line 194-231)
   ├─ Duplicate Detection (Line 233-246)
   └─ Reset Duplicate (Line 248+)

═══════════════════════════════════════════════════════════════════════════════════
🧠 SUPPORTING SERVICES
═══════════════════════════════════════════════════════════════════════════════════

backend/app/services/
├─ audit_service.py (Activity logging)
├─ duplicate_detection.py (Duplicate prevention)
├─ email_service.py (Notification sending)
└─ Status: ✅ ALL INTEGRATED

backend/app/ai/
├─ engine.py
│  ├─ load_ai_memory(db) - Dynamic reload
│  ├─ process_face(frame) - Real-time matching
│  ├─ face_recognition integration
│  └─ 128D embedding extraction
└─ Status: ✅ ACTIVE

═══════════════════════════════════════════════════════════════════════════════════
⚙️ CONFIGURATION & CORE
═══════════════════════════════════════════════════════════════════════════════════

backend/app/core/
├─ auth.py
│  ├─ create_access_token()
│  ├─ decode_token()
│  ├─ verify_password() [Bcrypt]
│  ├─ get_password_hash() [Bcrypt]
│  └─ Status: ✅ TOKEN SYSTEM WORKING
│
├─ config.py
│  ├─ Settings (BaseSettings)
│  ├─ SECRET_KEY, ALGORITHM, TOKEN_EXPIRE
│  └─ Status: ✅ CONFIGURED
│
├─ cache.py (Redis)
│  └─ Status: ✅ FACE ENCODING CACHE ACTIVE
│
└─ security.py
   └─ Security utilities

═══════════════════════════════════════════════════════════════════════════════════
✅ SUMMARY: WHERE EVERYTHING IS LOCATED
═══════════════════════════════════════════════════════════════════════════════════

BROADCAST (Notice):
  📍 backend/app/api/v1/endpoints/admin.py - Lines 90-103
  🔐 Role: ADMIN
  📌 Endpoint: POST /api/v1/admin/notice

ANALYTICS:
  📍 backend/app/api/v1/endpoints/admin.py - Lines 25-42
  🔐 Role: ADMIN
  📌 Endpoint: GET /api/v1/admin/analytics

ENROLLMENT:
  📍 backend/app/api/v1/endpoints/admin.py - Lines 47-86
  🔐 Role: TEACHER/ADMIN
  📌 Endpoint: POST /api/v1/admin/enroll

ATTENDANCE MARKING:
  📍 backend/app/api/v1/endpoints/attendance.py - Lines 16+
  🔐 Role: ALL
  📌 Endpoint: WS /api/v1/attendance/ws

EXPORT DATA:
  📍 backend/app/api/v1/endpoints/admin.py - Lines 124-220
  🔐 Role: ADMIN
  📌 Endpoint: GET /api/v1/admin/export

DUTY LEAVE:
  📍 backend/app/api/v1/endpoints/admin.py - Lines 103-122
  🔐 Role: TEACHER/ADMIN
  📌 Endpoint: POST /api/v1/admin/grant-dl

AUTHENTICATION:
  📍 backend/app/api/v1/endpoints/auth.py - Lines 18-122
  🔐 Various endpoints
  📌 JWT tokens, Bcrypt security, RBAC

BIOMETRIC ENGINE:
  📍 backend/app/ai/engine.py
  🔐 Integration with OpenCV & face_recognition
  📌 Real-time 128D embedding matching

FRONTEND:
  📍 frontend/templates/index.html (Main dashboard)
  📍 frontend/templates/login.html (Authentication)
  📍 frontend/templates/dashboard.html (Admin)
  🎨 Glass morphism design with real-time WebSocket

═══════════════════════════════════════════════════════════════════════════════════

All features are LIVE and INTEGRATED ✅
Dashboard screenshot shows real-time system operating normally!

