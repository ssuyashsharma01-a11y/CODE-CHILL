import json
from datetime import datetime, timedelta
from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy import func

from ....db.session import get_db
from ....models.domain import User, Notice, Attendance, Activity
from ....schemas.validation import UserEnroll, NoticeCreate
from ....core.auth import TokenData
from ....ai.engine import bio_engine
from . import auth

router = APIRouter(tags=["admin-operations"])

TRASH_SUBJECTS = ["FULL_DAY_DL", "EXPO_PLATINUM_DEMO", "GENERAL_DL", "SYSTEM_TEST"]

# =========================
# 📊 LIVE ANALYTICS (Optimized 🔥)
# =========================
@router.get("/analytics-live")
async def get_live_analytics(db: Session = Depends(get_db)):
    try:
        total_students = db.query(User).filter(User.role == "STUDENT").count()
        
        # Fast Aggregation using Case-When
        stats = db.query(
            Attendance.uid,
            func.count(Attendance.id).label("total"),
            func.sum(func.case([(Attendance.status.in_(["VERIFIED", "DUTY_LEAVE"]), 1)], else_=0)).label("present")
        ).filter(Attendance.subject.not_in(TRASH_SUBJECTS)).group_by(Attendance.uid).all()

        shortage = 0
        total_pct = 0
        valid_students = 0

        for s in stats:
            if s.total == 0: continue
            pct = (s.present / s.total) * 100
            total_pct += pct
            valid_students += 1
            if pct < 75: shortage += 1

        avg_attendance = (total_pct / valid_students) if valid_students else 0

        return {
            "total_enrolled": total_students,
            "avg_attendance": round(avg_attendance, 1),
            "shortage_alerts": shortage,
            "system_status": "SOVEREIGN_ACTIVE"
        }
    except Exception as e:
        raise HTTPException(500, str(e))

# =========================
# 📜 ATTENDANCE HISTORY (NEW 🚀)
# =========================
@router.get("/attendance/history")
async def get_attendance_history(db: Session = Depends(get_db), 
                                 current_user: TokenData = Depends(auth.require_teacher_admin)):
    """Fetches global history for the dashboard modal."""
    try:
        logs = db.query(Attendance).order_by(Attendance.timestamp.desc()).limit(100).all()
        return [
            {
                "id": log.id,
                "uid": log.uid,
                "subject": log.subject,
                "status": log.status,
                "timestamp": log.timestamp
            } for log in logs
        ]
    except Exception as e:
        raise HTTPException(500, str(e))

# =========================
# 📢 NOTICE SYSTEM (With Delete 🔥)
# =========================
@router.post("/notice")
async def create_notice(data: NoticeCreate,
                        db: Session = Depends(get_db),
                        current_user: TokenData = Depends(auth.require_teacher_admin)):
    try:
        notice = Notice(
            title="Broadcast",
            content=data.content,
            is_urgent=data.is_urgent,
            created_by=current_user.uid,
            created_at=datetime.now()
        )
        db.add(notice)
        db.commit()
        return {"status": "success"}
    except Exception as e:
        db.rollback()
        raise HTTPException(500, str(e))

@router.delete("/broadcast/notices/{notice_id}")
async def delete_notice(notice_id: int, 
                        db: Session = Depends(get_db),
                        current_user: TokenData = Depends(auth.require_teacher_admin)):
    """Deletes a broadcast notice from the matrix."""
    try:
        notice = db.query(Notice).filter(Notice.id == notice_id).first()
        if not notice:
            raise HTTPException(404, "Notice not found")
        db.delete(notice)
        db.commit()
        return {"status": "success"}
    except Exception as e:
        db.rollback()
        raise HTTPException(500, str(e))

@router.get("/broadcast/notices")
async def get_active_notices(db: Session = Depends(get_db)):
    """Public endpoint for everyone to see active signals."""
    notices = db.query(Notice).order_by(Notice.created_at.desc()).all()
    return notices

# =========================
# 🎓 SAFE DL ENGINE (Bulk Injection)
# =========================
@router.post("/grant-dl-bulk")
async def grant_dl(payload: dict = Body(...),
                   db: Session = Depends(get_db),
                   current_user: TokenData = Depends(auth.require_teacher_admin)):

    uid = payload.get("uid")
    subject = payload.get("subject", "GENERAL_DL")
    start = payload.get("start_date")
    end = payload.get("end_date") or start

    if not uid or not start:
        raise HTTPException(400, "UID and Start Date required")

    user = db.query(User).filter(User.uid == uid.upper()).first()
    if not user:
        raise HTTPException(404, "User not found")

    start_dt = datetime.strptime(start, "%Y-%m-%d")
    end_dt = datetime.strptime(end, "%Y-%m-%d")
    count = 0

    try:
        while start_dt <= end_dt:
            # Weekend Skip Logic
            if start_dt.weekday() < 6: # Skip Sunday
                exists = db.query(Attendance).filter(
                    Attendance.uid == uid,
                    Attendance.timestamp >= start_dt,
                    Attendance.timestamp < start_dt + timedelta(days=1)
                ).first()

                if not exists:
                    db.add(Attendance(
                        uid=uid,
                        subject=subject,
                        status="DUTY_LEAVE",
                        lecture_slot="ADMIN_INJECTED",
                        timestamp=start_dt.replace(hour=9, minute=0)
                    ))
                    count += 1
            start_dt += timedelta(days=1)

        db.add(Activity(action=f"BULK_DL_GRANT {uid}", user_id=uid, admin_id=current_user.uid))
        db.commit()
        return {"status": "success", "records": count}
    except Exception as e:
        db.rollback()
        raise HTTPException(500, str(e))

# =========================
# 🎓 ENROLLMENT
# =========================
@router.post("/enroll")
async def enroll_student(data: UserEnroll,
                         db: Session = Depends(get_db),
                         current_user: TokenData = Depends(auth.require_teacher_admin)):
    try:
        user = User(
            uid=data.uid.upper(),
            name=data.name,
            password_hash="TEMP_ACCESS",
            encoding=json.dumps([0.0] * 128),
            role="STUDENT"
        )
        db.merge(user)
        db.commit()
        bio_engine.load_ai_memory(db) # Hot-reload RAM
        return {"status": "success"}
    except Exception as e:
        db.rollback()
        raise HTTPException(500, str(e))