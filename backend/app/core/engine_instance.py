import logging
import time
from threading import Lock
from datetime import datetime, timedelta
from ..ai.engine import bio_engine
from ..models.domain import Attendance

logger = logging.getLogger("TrustMark-Engine")

_engine_lock = Lock()
engine_ai = bio_engine

def get_engine():
    if engine_ai is None:
        raise RuntimeError("Engine not initialized")
    return engine_ai

def initialize_sovereign_memory(db_session):
    """Initializes the AI RAM with enrolled face encodings."""
    start = time.time()
    try:
        logger.info("ENGINE_BOOT_START: Synchronizing Identities...")
        with _engine_lock:
            engine_ai.load_ai_memory(db_session)

        count = len(engine_ai.known_uids)
        duration = round(time.time() - start, 2)

        logger.info({
            "event": "ENGINE_READY",
            "identities": count,
            "boot_time": f"{duration}s"
        })
    except Exception as e:
        logger.error(f"ENGINE_FAIL: {e}")
        raise RuntimeError("Engine init failed") from e

# --- 📜 NEW: HISTORY & ANALYTICS HELPER ---
def get_attendance_history(db_session, uid=None, limit=50):
    """
    Fetches attendance logs. 
    If UID is provided, fetches specific history, else fetches global logs for admin.
    """
    query = db_session.query(Attendance)
    if uid:
        query = query.filter(Attendance.uid == uid)
    
    # Latest first (Day-wise sorting)
    logs = query.order_by(Attendance.timestamp.desc()).limit(limit).all()
    
    return [
        {
            "uid": log.uid,
            "subject": log.subject,
            "timestamp": log.timestamp.isoformat(),
            "status": log.status
        } for log in logs
    ]

# --- 🎓 NEW: BULK DL INJECTION ENGINE ---
def inject_bulk_attendance(db_session, uid, subject, start_date, end_date):
    """
    Forcefully injects attendance records into the database for a given range.
    Handles 'ALL' subjects by matching with timetable logic.
    """
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        current = start
        added_count = 0
        
        while current <= end:
            # Skip Sundays (Sovereign Matrix doesn't record on Sundays)
            if current.weekday() != 6:
                new_log = Attendance(
                    uid=uid,
                    subject=subject if subject != "ALL" else "SOVEREIGN_BULK_DL",
                    timestamp=current.replace(hour=9, minute=0), # Standard shift start
                    status="VERIFIED_DL",
                    lecture_slot="BULK_INJECTION"
                )
                db_session.add(new_log)
                added_count += 1
            current += timedelta(days=1)
        
        db_session.commit()
        return added_count
    except Exception as e:
        db_session.rollback()
        logger.error(f"BULK_INJECTION_FAILED: {e}")
        return 0

def refresh_memory(db_session):
    logger.info("Refreshing AI memory...")
    initialize_sovereign_memory(db_session)

def health_status():
    try:
        count = len(engine_ai.known_uids)
        return {
            "status": "READY" if count else "EMPTY",
            "identities": count,
            "pipeline": "ACTIVE"
        }
    except:
        return {"status": "ERROR"}