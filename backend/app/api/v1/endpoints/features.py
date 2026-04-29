import json
import math
from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy import func

from ....db.session import get_db
from ....models.domain import (
    Notice, User, Attendance, Activity, 
    TimeTable, DutyLeave, BroadcastMessage
)
from ....schemas.validation import (
    NoticeCreate, NoticeResponse,
    TimeTableCreate, TimeTableResponse,
    DutyLeaveRequest, DutyLeaveResponse
)
from ....core.auth import TokenData

# 🛡️ EXPLICIT IMPORTS: Hitting the file directly to avoid 'router' attribute errors
from .auth import require_teacher_admin, require_admin, get_current_user as require_auth

router = APIRouter(tags=["sovereign-features"])

# =========================
# 📢 BROADCAST ENGINE
# =========================

@router.post("/broadcast/notice", response_model=NoticeResponse)
async def create_broadcast_notice(
    data: NoticeCreate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(require_teacher_admin) # 👈 Updated
):
    try:
        notice = Notice(
            title=data.title or "Matrix Broadcast",
            content=data.content,
            is_urgent=data.is_urgent,
            created_by=current_user.uid,
            broadcast_status="DEPLOYED",
            target_role=data.target_role or "ALL",
            created_at=datetime.now()
        )
        db.add(notice)
        db.commit()
        
        db.add(Activity(
            action=f"📢 SIGNAL_DEPLOYED: {data.content[:20]}...",
            action_type="BROADCAST",
            admin_id=current_user.uid
        ))
        db.commit()
        return notice
    except Exception as e:
        db.rollback()
        raise HTTPException(400, str(e))

@router.delete("/broadcast/notice/{notice_id}")
async def delete_broadcast_notice(
    notice_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(require_teacher_admin)
):
    try:
        notice = db.query(Notice).filter(Notice.id == notice_id).first()
        if not notice:
            raise HTTPException(404, "Signal not found")
        db.delete(notice)
        db.commit()
        return {"status": "TERMINATED"}
    except Exception as e:
        db.rollback()
        raise HTTPException(500, str(e))

# =========================
# 📊 ATTENDANCE ANALYTICS
# =========================

@router.get("/attendance/{uid}")
async def get_student_attendance(
    uid: str,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(require_auth) # 👈 Updated
):
    uid = uid.upper()
    student = db.query(User).filter(User.uid == uid).first()
    if not student:
        raise HTTPException(404, "Student not found")

    records = db.query(Attendance).filter(Attendance.uid == uid).all()
    by_subject = {}

    for r in records:
        sub = r.subject
        by_subject.setdefault(sub, {"total": 0, "present": 0})
        by_subject[sub]["total"] += 1
        if r.status in ["VERIFIED", "DUTY_LEAVE"]:
            by_subject[sub]["present"] += 1

    result = []
    for sub, data in by_subject.items():
        pct = (data["present"] / data["total"]) * 100 if data["total"] else 0
        result.append({
            "subject": sub,
            "total": data["total"],
            "present": data["present"],
            "attendance_percentage": round(pct, 2)
        })

    return {
        "uid": student.uid,
        "name": student.name,
        "subjects": result,
        "overall": round(sum(r['attendance_percentage'] for r in result)/len(result), 2) if result else 0
    }

# =========================
# 🏥 DUTY LEAVE ENGINE
# =========================

@router.post("/duty-leave/grant", response_model=DutyLeaveResponse)
async def grant_duty_leave(
    data: DutyLeaveRequest,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(require_teacher_admin)
):
    try:
        dl = DutyLeave(
            uid=data.uid.upper(),
            subject=data.subject,
            date=data.date,
            reason=data.reason,
            granted_by=current_user.uid,
            is_valid=True
        )
        db.add(dl)
        
        db.add(Attendance(
            uid=data.uid.upper(),
            subject=data.subject,
            timestamp=datetime.combine(data.date, datetime.min.time()),
            status="DUTY_LEAVE"
        ))

        db.commit()
        return dl
    except Exception as e:
        db.rollback()
        raise HTTPException(400, str(e))

# =========================
# 🛡️ AUDIT LOGS
# =========================

@router.get("/audit/logs")
async def audit_logs(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(require_admin),
    limit: int = 50
):
    logs = db.query(Activity).order_by(Activity.timestamp.desc()).limit(limit).all()
    return [{"action": l.action, "type": l.action_type, "time": l.timestamp} for l in logs]