╔════════════════════════════════════════════════════════════════════════════════╗
║                   📡 COMPLETE API REFERENCE GUIDE                              ║
║              How to Use Every Feature - Code Examples Included                  ║
╚════════════════════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════════════════════
🔑 1. AUTHENTICATION FEATURES
═══════════════════════════════════════════════════════════════════════════════════

1️⃣ LOGIN
──────────────────────────────────────────────────────────────────────────────────
POST /api/v1/auth/login

Headers:
  Content-Type: application/x-www-form-urlencoded

Body (Form Data):
  username: 25BAI70757        (format: CU UID in uppercase)
  password: trustmark_secure  (bcrypt hashed)

JavaScript Example:
┌────────────────────────────────────────────────────────────────────────────┐
│ const response = await fetch('/api/v1/auth/login', {                      │
│   method: 'POST',                                                         │
│   body: new URLSearchParams({                                             │
│     username: '25BAI70757',                                               │
│     password: 'trustmark_secure'                                          │
│   })                                                                       │
│ });                                                                        │
│                                                                            │
│ // Returns: Redirects to /api/v1/auth/index (Dashboard)                 │
│ // Sets HttpOnly cookie with JWT token                                   │
└────────────────────────────────────────────────────────────────────────────┘

Response: 302 Redirect to /api/v1/auth/index
Cookie: access_token=<JWT_TOKEN> (HttpOnly, 1440 min expiry)

───────────────────────────────────────────────────────────────────────────────

2️⃣ LOGOUT
──────────────────────────────────────────────────────────────────────────────────
GET /api/v1/auth/logout

JavaScript Example:
┌────────────────────────────────────────────────────────────────────────────┐
│ const response = await fetch('/api/v1/auth/logout', {                    │
│   method: 'GET',                                                         │
│   credentials: 'include'  // Include cookies                             │
│ });                                                                        │
│ // Session terminated, redirects to login page                           │
└────────────────────────────────────────────────────────────────────────────┘

Response: 302 Redirect to login page
Effect: Invalidates JWT token, clears session

───────────────────────────────────────────────────────────────────────────────

3️⃣ WHO AM I
──────────────────────────────────────────────────────────────────────────────────
GET /api/v1/auth/whoami

Headers:
  Cookie: access_token=<JWT_TOKEN>

Response:
┌────────────────────────────────────────────────────────────────────────────┐
│ {                                                                          │
│   "uid": "25BAI70757",                                                    │
│   "role": "ADMIN"                                                         │
│ }                                                                          │
└────────────────────────────────────────────────────────────────────────────┘

JavaScript Example:
┌────────────────────────────────────────────────────────────────────────────┐
│ const user = await (await fetch('/api/v1/auth/whoami')).json();          │
│ console.log(user.uid, user.role);                                         │
│ // Output: 25BAI70757 ADMIN                                               │
└────────────────────────────────────────────────────────────────────────────┘

───────────────────────────────────────────────────────────────────────────────

4️⃣ CHANGE PASSWORD
──────────────────────────────────────────────────────────────────────────────────
POST /api/v1/auth/change-password

Headers:
  Content-Type: application/json
  Cookie: access_token=<JWT_TOKEN>

Body:
{
  "current_password": "old_password",
  "new_password": "new_password_123"
}

Response:
┌────────────────────────────────────────────────────────────────────────────┐
│ {                                                                          │
│   "status": "success",                                                    │
│   "message": "Password updated"                                           │
│ }                                                                          │
└────────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════════
🎯 2. ADMIN FEATURES
═══════════════════════════════════════════════════════════════════════════════════

1️⃣ GET ANALYTICS
──────────────────────────────────────────────────────────────────────────────────
GET /api/v1/admin/analytics

Role Required: ADMIN

Headers:
  Cookie: access_token=<JWT_TOKEN>

Response:
┌────────────────────────────────────────────────────────────────────────────┐
│ {                                                                          │
│   "users": 25,                   // Total enrolled students               │
│   "notices": 12,                 // Total notices sent                    │
│   "today_records": 89,           // Today's attendance count              │
│   "recent": [                                                            │
│     {                                                                     │
│       "id": 1,                                                           │
│       "action": "📡 AUTH_SUCCESS: 25BAI70757",                          │
│       "user": "25BAI70757"                                              │
│     },                                                                    │
│     {                                                                     │
│       "id": 2,                                                           │
│       "action": "📢 BROADCAST: Important notice about...",              │
│       "user": "ADMIN"                                                   │
│     },                                                                    │
│     {                                                                     │
│       "id": 3,                                                           │
│       "action": "👤 IDENTITY_ENROLLED: 25BAI70758",                      │
│       "user": "25BAI70757"                                               │
│     }                                                                     │
│   ]                                                                       │
│ }                                                                          │
└────────────────────────────────────────────────────────────────────────────┘

JavaScript Example:
┌────────────────────────────────────────────────────────────────────────────┐
│ const analytics = await (await fetch('/api/v1/admin/analytics')).json(); │
│ console.log(`Total Users: ${analytics.users}`);                           │
│ console.log(`Today's Attendance: ${analytics.today_records}`);            │
│ // Output: Total Users: 25                                               │
│ //         Today's Attendance: 89                                        │
└────────────────────────────────────────────────────────────────────────────┘

───────────────────────────────────────────────────────────────────────────────

2️⃣ SEND BROADCAST NOTICE ⭐
──────────────────────────────────────────────────────────────────────────────────
POST /api/v1/admin/notice

Role Required: ADMIN

Headers:
  Content-Type: application/json
  Cookie: access_token=<JWT_TOKEN>

Body:
{
  "content": "All students should submit their assignments by Friday",
  "is_urgent": true
}

Response:
┌────────────────────────────────────────────────────────────────────────────┐
│ {                                                                          │
│   "status": "success",                                                    │
│   "message": "Signal Deployed"                                            │
│ }                                                                          │
└────────────────────────────────────────────────────────────────────────────┘

JavaScript Example:
┌────────────────────────────────────────────────────────────────────────────┐
│ const broadcast = await fetch('/api/v1/admin/notice', {                 │
│   method: 'POST',                                                         │
│   headers: { 'Content-Type': 'application/json' },                       │
│   body: JSON.stringify({                                                  │
│     content: 'Emergency: Campus will be closed tomorrow',               │
│     is_urgent: true                                                      │
│   })                                                                       │
│ }).then(r => r.json());                                                  │
│                                                                            │
│ console.log(broadcast.message); // "Signal Deployed"                     │
└────────────────────────────────────────────────────────────────────────────┘

Side Effects:
  ✓ Notice saved to database (Notice table)
  ✓ Audit log created (Activity table: "📢 BROADCAST: ...")
  ✓ Can be retrieved by students in dashboard

───────────────────────────────────────────────────────────────────────────────

3️⃣ ENROLL STUDENT
──────────────────────────────────────────────────────────────────────────────────
POST /api/v1/admin/enroll

Role Required: TEACHER/ADMIN

Headers:
  Content-Type: application/json
  Cookie: access_token=<JWT_TOKEN>

Body:
{
  "uid": "25BAI70758",
  "name": "John Smith",
  "face_encoding": [0.123, -0.456, 0.789, ...]  // 128-dimensional array
}

Response:
┌────────────────────────────────────────────────────────────────────────────┐
│ {                                                                          │
│   "status": "success",                                                    │
│   "message": "Student enrolled successfully"                              │
│ }                                                                          │
└────────────────────────────────────────────────────────────────────────────┘

Side Effects:
  ✓ User saved to database
  ✓ 128D face encoding stored (JSON serialized)
  ✓ AI memory dynamically reloaded (instant recognition available)
  ✓ Audit log: "👤 IDENTITY_ENROLLED: 25BAI70758"

Error Cases:
  ❌ "Neural capture failed: No face detected" (face validation failed)
  ❌ 400 Bad Request (invalid data)
  ❌ 403 Forbidden (insufficient role)

───────────────────────────────────────────────────────────────────────────────

4️⃣ GRANT DUTY LEAVE (DL)
──────────────────────────────────────────────────────────────────────────────────
POST /api/v1/admin/grant-dl

Role Required: TEACHER/ADMIN

Headers:
  Content-Type: application/json
  Cookie: access_token=<JWT_TOKEN>

Body:
{
  "uid": "25BAI70757",
  "subject": "DSA",
  "reason": "Medical appointment"  // Optional
}

Response:
┌────────────────────────────────────────────────────────────────────────────┐
│ {                                                                          │
│   "status": "success",                                                    │
│   "message": "Duty Leave Logged in Matrix"                               │
│ }                                                                          │
└────────────────────────────────────────────────────────────────────────────┘

Side Effects:
  ✓ Attendance record created with status="DUTY_LEAVE"
  ✓ Audit log: "🏥 DL_PROVISIONED: 25BAI70757"
  ✓ Exempt from attendance for that subject on that date

Restrictions:
  ⏱️ Only works Jan-May (CU semester lock)
  🚫 Returns 403 if not in DL season

───────────────────────────────────────────────────────────────────────────────

5️⃣ EXPORT ATTENDANCE DATA
──────────────────────────────────────────────────────────────────────────────────
GET /api/v1/admin/export

Role Required: ADMIN

Headers:
  Cookie: access_token=<JWT_TOKEN>

Response: CSV File
┌────────────────────────────────────────────────────────────────────────────┐
│ uid,name,subject,status,timestamp                                         │
│ 25BAI70757,John Doe,DSA,VERIFIED,2026-04-15 10:30:45                    │
│ 25BAI70758,Jane Smith,DSA,VERIFIED,2026-04-15 10:35:12                  │
│ 25BAI70759,Bob Johnson,DSA,DUPLICATE,2026-04-15 11:00:00                │
│ 25BAI70757,John Doe,DBMS,DUTY_LEAVE,2026-04-15 14:15:30                 │
└────────────────────────────────────────────────────────────────────────────┘

File Name: attendance_export_<timestamp>.csv

JavaScript Example:
┌────────────────────────────────────────────────────────────────────────────┐
│ const link = document.createElement('a');                                 │
│ link.href = '/api/v1/admin/export';                                       │
│ link.download = 'attendance.csv';                                         │
│ link.click();                                                              │
│ // Downloads CSV file to user's computer                                  │
└────────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════════
🎥 3. BIOMETRIC / ATTENDANCE FEATURES
═══════════════════════════════════════════════════════════════════════════════════

1️⃣ REAL-TIME BIOMETRIC MARKING (WebSocket)
──────────────────────────────────────────────────────────────────────────────────
WS /api/v1/attendance/ws

Type: WebSocket (Real-time bidirectional)
Role: ALL USERS

Connection:
┌────────────────────────────────────────────────────────────────────────────┐
│ const ws = new WebSocket('ws://localhost/api/v1/attendance/ws');         │
│                                                                            │
│ ws.onopen = () => {                                                       │
│   console.log('Connected to biometric stream');                           │
│ };                                                                         │
│                                                                            │
│ ws.onmessage = (event) => {                                              │
│   const data = JSON.parse(event.data);                                   │
│   console.log(data);  // {match: "25BAI70757"} or {status: "ANALYZING"}│
│ };                                                                         │
│                                                                            │
│ ws.onerror = (error) => {                                                │
│   console.error('WebSocket error:', error);                              │
│ };                                                                         │
└────────────────────────────────────────────────────────────────────────────┘

Sending Video Frame:
┌────────────────────────────────────────────────────────────────────────────┐
│ // Get video frame from canvas                                            │
│ const canvas = document.querySelector('canvas');                          │
│ const frameData = canvas.toDataURL('image/jpeg');  // Base64             │
│                                                                            │
│ ws.send(JSON.stringify({                                                  │
│   type: 'frame',                                                          │
│   data: frameData                                                         │
│ }));                                                                        │
└────────────────────────────────────────────────────────────────────────────┘

Receiving Response:
┌────────────────────────────────────────────────────────────────────────────┐
│ Success Response:                                                          │
│ {                                                                          │
│   "status": "MATCHED",                                                    │
│   "uid": "25BAI70757",                                                    │
│   "name": "John Doe",                                                     │
│   "confidence": 0.95,                                                     │
│   "subject": "DSA",                                                       │
│   "timestamp": "2026-04-15 10:30:45"                                      │
│ }                                                                          │
│                                                                            │
│ No Match Response:                                                         │
│ {                                                                          │
│   "status": "NO_MATCH",                                                   │
│   "message": "Face not recognized"                                        │
│ }                                                                          │
│                                                                            │
│ Duplicate Detection Response:                                              │
│ {                                                                          │
│   "status": "DUPLICATE",                                                  │
│   "message": "Attendance already marked in last 2 hours"                 │
│ }                                                                          │
└────────────────────────────────────────────────────────────────────────────┘

Process Flow:
┌──────────────────────────────────────────────────────────────────────────┐
│ 1. Client sends video frame                                             │
│ 2. Server captures frame                                                │
│ 3. Face detection: face_recognition.face_locations()                    │
│ 4. Extract encoding: face_recognition.face_encodings() → 128D array     │
│ 5. Compare to enrolled faces: face_recognition.compare_faces()          │
│ 6. Check for duplicates                                                 │
│ 7. Return match result or "NO_MATCH"                                    │
│ 8. If matched: Auto-mark attendance                                     │
│ 9. Update real-time roster on dashboard                                 │
└──────────────────────────────────────────────────────────────────────────┘

───────────────────────────────────────────────────────────────────────────────

2️⃣ GET ATTENDANCE HISTORY
──────────────────────────────────────────────────────────────────────────────────
GET /api/v1/attendance/history?skip=0&limit=10

Headers:
  Cookie: access_token=<JWT_TOKEN>

Query Parameters:
  skip: 0 (start from record 0)
  limit: 10 (get 10 records)

Response:
┌────────────────────────────────────────────────────────────────────────────┐
│ [                                                                          │
│   {                                                                        │
│     "id": 1,                                                              │
│     "uid": "25BAI70757",                                                  │
│     "name": "John Doe",                                                   │
│     "subject": "DSA",                                                     │
│     "status": "VERIFIED",                                                 │
│     "timestamp": "2026-04-15 10:30:45",                                   │
│     "face_match_score": 0.95                                              │
│   },                                                                       │
│   {                                                                        │
│     "id": 2,                                                              │
│     "uid": "25BAI70758",                                                  │
│     "name": "Jane Smith",                                                 │
│     "subject": "DSA",                                                     │
│     "status": "VERIFIED",                                                 │
│     "timestamp": "2026-04-15 10:35:12",                                   │
│     "face_match_score": 0.92                                              │
│   }                                                                        │
│ ]                                                                          │
└────────────────────────────────────────────────────────────────────────────┘

JavaScript Example:
┌────────────────────────────────────────────────────────────────────────────┐
│ const history = await (await fetch(                                      │
│   '/api/v1/attendance/history?skip=0&limit=10'                           │
│ )).json();                                                                │
│                                                                            │
│ history.forEach(record => {                                              │
│   console.log(                                                            │
│     `${record.name} (${record.uid}): ${record.subject} - ${record.status}`
│   );                                                                       │
│ });                                                                        │
└────────────────────────────────────────────────────────────────────────────┘

───────────────────────────────────────────────────────────────────────────────

3️⃣ GET ATTENDANCE SUMMARY
──────────────────────────────────────────────────────────────────────────────────
GET /api/v1/attendance/summary

Role Required: ADMIN

Response:
┌────────────────────────────────────────────────────────────────────────────┐
│ {                                                                          │
│   "total_records": 150,                                                   │
│   "by_status": {                                                          │
│     "VERIFIED": 140,                                                      │
│     "DUPLICATE": 8,                                                       │
│     "DUTY_LEAVE": 2                                                       │
│   },                                                                       │
│   "by_subject": {                                                         │
│     "DSA": 48,                                                            │
│     "DBMS": 51,                                                           │
│     "OOP": 51                                                             │
│   },                                                                       │
│   "top_performers": [                                                     │
│     {"uid": "25BAI70757", "count": 28, "percentage": 100.0},             │
│     {"uid": "25BAI70758", "count": 26, "percentage": 92.8}               │
│   ]                                                                        │
│ }                                                                          │
└────────────────────────────────────────────────────────────────────────────┘

───────────────────────────────────────────────────────────────────────────────

4️⃣ GET DUPLICATE ATTEMPTS
──────────────────────────────────────────────────────────────────────────────────
GET /api/v1/attendance/duplicates

Role Required: ADMIN

Response:
┌────────────────────────────────────────────────────────────────────────────┐
│ [                                                                          │
│   {                                                                        │
│     "uid": "25BAI70759",                                                  │
│     "name": "Bob Johnson",                                                │
│     "subject": "DSA",                                                     │
│     "attempt_count": 3,                                                   │
│     "last_attempt": "2026-04-15 11:00:00",                               │
│     "status": "BLOCKED"                                                   │
│   }                                                                        │
│ ]                                                                          │
└────────────────────────────────────────────────────────────────────────────┘

───────────────────────────────────────────────────────────────────────────────

5️⃣ RESET DUPLICATE DETECTION
──────────────────────────────────────────────────────────────────────────────────
POST /api/v1/attendance/reset-duplicate/{uid}/{subject}

Role Required: ADMIN

Example: POST /api/v1/attendance/reset-duplicate/25BAI70759/DSA

Response:
┌────────────────────────────────────────────────────────────────────────────┐
│ {                                                                          │
│   "status": "success",                                                    │
│   "message": "Duplicate detection reset for 25BAI70759 - DSA"            │
│ }                                                                          │
└────────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════════
📱 4. FRONTEND PAGES
═══════════════════════════════════════════════════════════════════════════════════

1️⃣ LOGIN PAGE
─────────────────────────────────────────────────────────────────────────────────
URL: GET /api/v1/auth/login-page

Returns: HTML login form with:
  ├─ UID input field
  ├─ Password input field
  ├─ Submit button
  └─ Error message display

───────────────────────────────────────────────────────────────────────────────

2️⃣ MAIN DASHBOARD (Glass Morphism)
──────────────────────────────────────────────────────────────────────────────────
URL: GET /api/v1/auth/index

Access: Auto-redirect after login

Features Displayed:
  ├─ Header: Title, user info, logout button
  ├─ Main Section:
  │  ├─ Video feed (center-left) with face detection grid
  │  └─ "BIOMETRIC MATCH" indicator
  ├─ Right Sidebar:
  │  ├─ Registry count (animated number)
  │  ├─ "NEURAL ROSTER" list (live updating)
  │  ├─ "ENROLL IDENTITY" button
  │  └─ "EXPORT LOGS" button
  └─ Real-time WebSocket connection to attendance/ws

CSS Features:
  ├─ Glass morphism (backdrop-filter: blur)
  ├─ Neon cyan accents (#00ffff)
  ├─ Animated scan-line effect
  ├─ Pulsing indicators
  └─ Smooth transitions (0.3s ease)

Display Data:
  ├─ Current user UID & role
  ├─ Live roster with attendance badges
  ├─ Total enrolled count
  ├─ Real-time match notifications
  └─ WebSocket connection status

═══════════════════════════════════════════════════════════════════════════════════
🔐 SECURITY & AUTHENTICATION
═══════════════════════════════════════════════════════════════════════════════════

JWT Token Structure:
┌────────────────────────────────────────────────────────────────────────────┐
│ {                                                                          │
│   "uid": "25BAI70757",      // User identifier from CU system             │
│   "role": "ADMIN",           // Role (ADMIN, TEACHER, STUDENT)            │
│   "exp": 1713192000,         // Expiration timestamp (1440 minutes)       │
│   "iat": 1713105600          // Issued at timestamp                       │
│ }                                                                          │
│                                                                            │
│ Encoded: eyJhbGc... (Base64 encoded, HMAC-SHA256)                         │
│ Algorithm: HS256                                                           │
│ Secret: Loaded from .env (SECRET_KEY)                                    │
└────────────────────────────────────────────────────────────────────────────┘

Password Hashing:
┌────────────────────────────────────────────────────────────────────────────┐
│ Algorithm: Bcrypt (cost factor 10)                                         │
│ Storage: Hash stored in database (not plaintext)                           │
│ Verification: On login, entered password hashed and compared              │
│                                                                            │
│ Example hash: $2b$10$abcd1234efgh5678ijkl9012345678901234567890123456789  │
└────────────────────────────────────────────────────────────────────────────┘

RBAC Levels:
┌────────────────────────────────────────────────────────────────────────────┐
│ 🛡️  ADMIN (Full Control)                                                   │
│   ├─ Analytics (GET /admin/analytics)                                     │
│   ├─ Broadcast (POST /admin/notice)                                       │
│   ├─ Export (GET /admin/export)                                           │
│   ├─ Enroll students (POST /admin/enroll)                                │
│   ├─ Grant duty leave (POST /admin/grant-dl)                             │
│   ├─ Reset duplicate detection                                            │
│   └─ View all attendance records                                          │
│                                                                            │
│ 👨‍🏫 TEACHER (Limited Control)                                              │
│   ├─ Enroll students (POST /admin/enroll)                                │
│   ├─ Grant duty leave (POST /admin/grant-dl)                             │
│   └─ View attendance history                                              │
│                                                                            │
│ 👨‍🎓 STUDENT (View Only)                                                     │
│   ├─ Mark attendance via WebSocket                                        │
│   ├─ View own attendance                                                  │
│   └─ View broadcasts/notices                                              │
└────────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════════
💾 DATABASE SCHEMA
═══════════════════════════════════════════════════════════════════════════════════

User Table:
┌────────────────────────────────────────────────────────────────────────────┐
│ Column             │ Type      │ Description                              │
├────────────────────────────────────────────────────────────────────────────┤
│ uid (PK)           │ VARCHAR   │ Unique student ID (CU format)            │
│ name               │ VARCHAR   │ Full name                                │
│ password_hash      │ VARCHAR   │ Bcrypt hashed password                   │
│ role               │ VARCHAR   │ ADMIN / TEACHER / STUDENT                │
│ encoding           │ TEXT      │ 128D face vector (JSON)                  │
│ created_at         │ DATETIME  │ Enrollment timestamp                     │
└────────────────────────────────────────────────────────────────────────────┘

Attendance Table:
┌────────────────────────────────────────────────────────────────────────────┐
│ Column             │ Type      │ Description                              │
├────────────────────────────────────────────────────────────────────────────┤
│ id (PK)            │ INTEGER   │ Auto-increment ID                        │
│ uid (FK)           │ VARCHAR   │ Student UID                              │
│ subject            │ VARCHAR   │ Subject name (DSA, DBMS, OOP)            │
│ timestamp          │ DATETIME  │ Attendance marked time                   │
│ status             │ VARCHAR   │ VERIFIED / DUPLICATE / DUTY_LEAVE        │
│ face_match_score   │ FLOAT     │ Confidence (0.0-1.0)                    │
└────────────────────────────────────────────────────────────────────────────┘

Notice Table:
┌────────────────────────────────────────────────────────────────────────────┐
│ Column             │ Type      │ Description                              │
├────────────────────────────────────────────────────────────────────────────┤
│ id (PK)            │ INTEGER   │ Auto-increment ID                        │
│ content            │ TEXT      │ Notice message                           │
│ is_urgent          │ BOOLEAN   │ Urgent flag                              │
│ created_at         │ DATETIME  │ Creation timestamp                       │
└────────────────────────────────────────────────────────────────────────────┘

Activity Table (Audit Log):
┌────────────────────────────────────────────────────────────────────────────┐
│ Column             │ Type      │ Description                              │
├────────────────────────────────────────────────────────────────────────────┤
│ id (PK)            │ INTEGER   │ Auto-increment ID                        │
│ action             │ TEXT      │ Action description                       │
│ user_id            │ VARCHAR   │ Who performed action                     │
│ timestamp          │ DATETIME  │ Action timestamp                         │
└────────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════════
🧪 QUICK TEST COMMANDS
═══════════════════════════════════════════════════════════════════════════════════

1. Test Login:
   curl -X POST http://localhost/api/v1/auth/login \
     -d "username=25BAI70757&password=trustmark_secure" \
     -H "Content-Type: application/x-www-form-urlencoded"

2. Test Analytics:
   curl -X GET http://localhost/api/v1/admin/analytics \
     -H "Cookie: access_token=<YOUR_JWT_TOKEN>"

3. Test Broadcast:
   curl -X POST http://localhost/api/v1/admin/notice \
     -H "Content-Type: application/json" \
     -d '{"content": "Test notice", "is_urgent": false}' \
     -H "Cookie: access_token=<YOUR_JWT_TOKEN>"

4. Test Export:
   curl -X GET http://localhost/api/v1/admin/export \
     -H "Cookie: access_token=<YOUR_JWT_TOKEN>" \
     -o attendance.csv

5. Test Attendance History:
   curl http://localhost/api/v1/attendance/history \
     -H "Cookie: access_token=<YOUR_JWT_TOKEN>"

═══════════════════════════════════════════════════════════════════════════════════

All features are LIVE, TESTED, and PRODUCTION READY! ✅

