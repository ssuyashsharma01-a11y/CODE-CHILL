# 🏫 CHANDIGARH UNIVERSITY TIMETABLE INTEGRATION

**Source**: Official CU JAN_MAY Semester Schedule (April 18, 2026)

---

## 📅 Time Slot Mapping

The actual CU schedule has been mapped to our **Morning/Lunch/Evening** slots:

| Time Slot | CU Classes | Lecture # | Our Slot | Attendance Status |
|-----------|-----------|-----------|----------|------------------|
| **09:30-10:20 AM** | Various courses | 1st Period | **Morning** | ✅ ACTIVE |
| **10:20-11:10 AM** | Various courses | 2nd Period | **Morning** | ✅ ACTIVE |
| **11:20 AM-12:10 PM** | Various courses | 3rd Period | **Morning** | ✅ ACTIVE |
| **12:10-01:00 PM** | Various courses | 4th Period | **Lunch** | 🍴 LOCKED |
| **01:05-01:55 PM** | Various courses | 5th Period | **Evening** | ✅ ACTIVE |
| **01:55-02:45 PM** | Various courses | 5th Period | **Evening** | ✅ ACTIVE |
| **02:45-03:35 PM** | Various courses | 6th Period | **Evening** | ✅ ACTIVE |

---

## 📊 Courses in Timetable

### Computer Science & Engineering (CSH)
- **25CSH-103**: Data Structures / Core CS Theory
  - Instructor: Pawandeep Kaur (E14374)
  - Room: C1-611
  - **Monday**: 09:30-11:10 AM (Morning)
  - **Tuesday**: 09:30-11:10 AM (Morning)
  - **Wednesday**: 11:20 AM-01:00 PM
  - **Friday**: 09:30-11:10 AM (Morning)

- **25CSH-105**: Database Systems
  - Instructor: Jaswinder Kaur (E2850)
  - Room: C1-303
  - **Monday-Tuesday**: 11:20 AM-01:00 PM

- **25CSH-111**: Web Technologies
  - Instructor: Paras Khullar (E3125)
  - Room: C1-416
  - **Friday**: 11:20 AM-01:00 PM

### Computer Programming (CPP)
- **25CPP-111**: Programming Fundamentals
  - Instructor: Jaspal Singh Bhindsa (E5432)
  - Rooms: C1-504, C1-604
  - **Wednesday**: 09:30-11:10 AM & 02:45-03:35 PM

### Social Media & Technology (SMT)
- **25SMT-198**: Tech Workshop
  - Instructor: Amit Kumar (E2309)
  - Rooms: C1-715, C1-715-A
  - **Monday-Friday**: Multiple sessions

### Electronics Engineering (CEP/EOH/MEP)
- **25CEP-102/101**: Physical Electronics
  - Instructors: Sudhir Kumar, Sachin
  - **Thursday**: Morning & Lunch slots

- **25EOH-101**: Environment & Health
  - Instructor: Sachin (E9435)
  - **Saturday**: Morning

- **25MEP-102**: Manufacturing Engineering
  - Instructor: Paras Khullar (E3125)
  - **Saturday**: Morning & Lunch

### Other Courses
- **25SZT-148**: Special Topic (Saturday Evening)
- **25TDP-151**: Technical Workshop (Thursday Afternoon)
- **25CEH-101**: Environmental Chemistry (Friday Evening)

---

## 🚀 How to Seed the Timetable

### Option 1: Run Python Script (Recommended)
```bash
cd backend/scripts
python seed_cu_timetable.py
```

**Output:**
```
✅ 25CSH-103 - Mon 09:30-10:20 (Morning)
✅ 25CSH-103 - Mon 10:20-11:10 (Morning)
✅ 25CSH-105 - Mon 11:20-12:10 (Morning)
...
✅ SUCCESS: 72 timetable entries loaded!
🏫 Chandigarh University timetable is now active in the system
```

### Option 2: Manual Database Entry
```sql
INSERT INTO time_tables (
  subject, day_of_week, start_time, end_time, lecture_number, 
  lecture_slot, semester_cycle, room, instructor
) VALUES
  ('25CSH-103', 0, '09:30:00', '10:20:00', 1, 'Morning', 'JAN_MAY', 'C1-611', 'Pawandeep Kaur'),
  ...
```

---

## 🔄 Attendance Validation Flow

When a student scans their biometric during a lecture:

```
1. BIOMETRIC SCAN (128D Face Embedding)
   ↓
2. CHECK CURRENT TIME
   09:30 AM → "Morning Slot" ✅
   12:00 PM → "Lunch Break" 🍴
   ↓
3. QUERY TIMETABLE
   SELECT * FROM time_tables WHERE
     subject = 'AI_IDENTITY_CORE' AND
     day_of_week = 0 (Monday) AND
     lecture_slot = 'Morning'
   ↓
4. RESULT: Lecture Found
   25CSH-103 with Pawandeep Kaur at C1-611 ✅
   ↓
5. CHECK DUTY LEAVE
   SELECT * FROM duty_leaves WHERE
     uid = 'STU_001' AND
     subject = '25CSH-103' AND
     date = TODAY AND
     is_valid = TRUE
   ↓
6. ATTENDANCE RECORDED
   Status: "VERIFIED" (or "DL_MARKED" if DL exists)
   Lecture Slot: "Morning"
   Audited: ✅
```

---

## ✅ Example Scenarios

### Scenario 1: Normal Attendance ✅
**Time**: Friday 09:45 AM  
**Subject**: 25CSH-103 Data Structures  
**Student**: STU_001  

**System Check**:
- Current time: 09:45 AM → Morning slot ✅
- Day: Friday (day_of_week = 4) ✅
- Timetable match found: Pawandeep Kaur in C1-611 ✅
- No DL: Regular attendance ✅

**Result**: `{"status": "SUCCESS", "count": 1/2, "lecture_slot": "Morning"}`

---

### Scenario 2: Outside Lecture Hours ❌
**Time**: 15:45 (3:45 PM)  
**Subject**: 25CSH-103  

**System Check**:
- Current time: 15:45 → Outside active hours ❌

**Result**: 
```json
{
  "status": "INACTIVE_SLOT",
  "message": "Attendance not allowed outside lecture hours. Current time: 15:45"
}
```

---

### Scenario 3: Lunch Break ❌
**Time**: 12:30 PM  
**Subject**: 25CSH-105  

**System Check**:
- Current time: 12:30 → Lunch break (12:10-01:00) 🍴
- Attendance locked during break ❌

**Result**: 
```json
{
  "status": "LUNCH_BREAK",
  "message": "Attendance locked during lunch break (12:00 PM - 1:00 PM)"
}
```

---

### Scenario 4: Duty Leave Override ✅
**Time**: Wednesday 10:00 AM  
**Subject**: 25CPP-111  
**Student**: STU_002 (has valid DL)  

**System Check**:
- Current time: 10:00 AM → Morning slot ✅
- Timetable match found ✅
- **DL Check**: Valid DL found for STU_002 on this date ✅

**Result**: 
```json
{
  "status": "SUCCESS",
  "dutyleave_status": "DL_APPROVED",
  "message": "Attendance marked with Duty Leave approval"
}
```

---

## 📱 Frontend Display Integration

### Current Lecture Widget
```javascript
// On dashboard load
GET /api/v1/sovereign/timetable/current-lecture?subject=25CSH-103

Response:
{
  "status": "ACTIVE",
  "subject": "25CSH-103",
  "lecture_number": 1,
  "lecture_slot": "Morning",
  "start_time": "09:30",
  "end_time": "10:20",
  "room": "C1-611",
  "instructor": "Pawandeep Kaur(E14374)",
  "current_time": "2026-04-18T09:45:00"
}

// Display on frontend:
🏫 Current Lecture: 25CSH-103
📍 Room: C1-611
👨‍🏫 Instructor: Pawandeep Kaur
⏰ Time: 09:30-10:20 AM (Morning Session)
```

### Timetable View
```javascript
// Weekly schedule
GET /api/v1/sovereign/timetable/subject/25CSH-103/semester/JAN_MAY

// Display all lectures for this course throughout the week
```

---

## 🔐 Security & Integrity

### Temporal Validation ✅
- Each attendance tied to specific lecture time window
- No attendance outside 09:30 AM - 03:35 PM
- Lunch break (12:10-01:00 PM) completely locked

### Academic Validation ✅
- Subject must exist in CU official timetable
- Lecture must be scheduled for that specific day/time
- Prevents attendance for non-existent lectures

### DL Integration ✅
- Duty leave overrides attendance requirement
- Only valid for JAN_MAY semester (Jan-May)
- All DL grants audited with admin ID

### Audit Trail ✅
- Every attendance logged with lecture_slot
- Action type recorded: ATTENDANCE_VERIFIED
- Timestamp preserved for official records

---

## 📋 Data Dictionary

### TimeTable Schema
```python
{
  "subject": "25CSH-103",              # Course code
  "day_of_week": 0,                    # 0=Mon, 1=Tue, ..., 6=Sun
  "start_time": "09:30:00",            # HH:MM:SS
  "end_time": "10:20:00",              # HH:MM:SS
  "lecture_number": 1,                 # 1-6 (period in day)
  "lecture_slot": "Morning",           # Morning/Lunch/Evening
  "semester_cycle": "JAN_MAY",         # JAN_MAY or JUL_NOV
  "room": "C1-611",                    # Classroom/Lab location
  "instructor": "Pawandeep Kaur(E14374)" # Name (ID)
}
```

---

## 🎯 Key Benefits

✅ **Accurate Attendance**: Validates against real CU schedule  
✅ **Prevents Gaming**: Can't mark attendance outside class hours  
✅ **Lunch Break Protection**: Automated break between morning/evening  
✅ **Duty Leave Integration**: DL seamlessly overrides requirement  
✅ **Complete Audit Trail**: Every action logged with time/admin  
✅ **Multi-Semester Support**: Easily switch between JAN_MAY and JUL_NOV  
✅ **Instructor Tracking**: Records who was teaching each class  

---

## 📞 Next Steps

1. **Run seed script**: `python backend/scripts/seed_cu_timetable.py`
2. **Verify database**: Query `time_tables` table (should have ~72 entries)
3. **Test API**: Call `/api/v1/sovereign/timetable/current-lecture`
4. **Deploy**: Update frontend to display current lecture info
5. **Monitor**: Check audit logs for attendance validation

**System Status**: 🟢 Ready for Production

---

**🏛️ TrustMark Sovereign v25 Platinum - CU Integration Complete 🏛️**
