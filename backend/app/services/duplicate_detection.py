"""
Sovereign Duplicate Governance Service - TrustMark AI Platinum
Prevents 'Double-Tap' identity fraud and temporal redundancy.
"""

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Tuple, List, Dict
import logging
from ..models.domain import Attendance

logger = logging.getLogger("TrustMark-DuplicateService")

class DuplicateDetectionService:
    """
    Sovereign Logic: Ensures that an identity can only occupy a 
    temporal slot once within the defined governance window.
    """
    
    # Window tuned for CU Expo environment (Fast-moving lines)
    DUPLICATE_WINDOW_MINUTES = 5 
    
    @staticmethod
    def check_duplicate_attendance(db: Session, uid: str, subject: str) -> Tuple[bool, str]:
        """
        Validates if the identity has already established a verified handshake.
        """
        # Temporal threshold check
        time_threshold = datetime.utcnow() - timedelta(minutes=DuplicateDetectionService.DUPLICATE_WINDOW_MINUTES)
        
        recent_log = db.query(Attendance).filter(
            Attendance.uid == uid,
            Attendance.subject == subject,
            Attendance.timestamp >= time_threshold,
            Attendance.status.in_(["VERIFIED", "DL_MARKED"]) # Don't allow if already verified or DL applied
        ).order_by(Attendance.timestamp.desc()).first()
        
        if recent_log:
            time_diff = (datetime.utcnow() - recent_log.timestamp).total_seconds() / 60
            remaining = DuplicateDetectionService.DUPLICATE_WINDOW_MINUTES - time_diff
            
            msg = f"🛡️ DUPLICATE_LOCK: Already marked {time_diff:.1f}m ago. Wait {remaining:.1f}m."
            logger.warning(f"⚠️ [DUPLICATE_ATTEMPT]: {uid} rejected for {subject}")
            return True, msg
        
        return False, "✅ IDENTITY_UNIQUE: Proceeding to Verification."
    
    @staticmethod
    def get_duplicate_attempts(db: Session, limit: int = 50) -> List[Dict]:
        """
        Fetches frequency analytics for the Sovereign Dashboard.
        Useful for identifying students attempting 'Ghost Attendance'.
        """
        from sqlalchemy import func, desc
        
        time_threshold = datetime.utcnow() - timedelta(minutes=DuplicateDetectionService.DUPLICATE_WINDOW_MINUTES)
        
        duplicates = db.query(
            Attendance.uid,
            Attendance.subject,
            func.count(Attendance.id).label("count"),
            func.max(Attendance.timestamp).label("last_attempt")
        ).filter(
            Attendance.timestamp >= time_threshold
        ).group_by(
            Attendance.uid,
            Attendance.subject
        ).having(
            func.count(Attendance.id) > 1
        ).order_by(desc("last_attempt")).limit(limit).all()
        
        return [
            {
                "uid": uid,
                "subject": subject,
                "duplicate_count": count,
                "last_attempt": last_attempt.isoformat() if last_attempt else None
            } 
            for uid, subject, count, last_attempt in duplicates
        ]
    
    @staticmethod
    def reset_duplicate_window(db: Session, uid: str, subject: str) -> bool:
        """
        Sovereign Override: Resets the identity window for specific cases.
        (Admin Clearance Required)
        """
        try:
            time_threshold = datetime.utcnow() - timedelta(minutes=DuplicateDetectionService.DUPLICATE_WINDOW_MINUTES)
            
            db.query(Attendance).filter(
                Attendance.uid == uid,
                Attendance.subject == subject,
                Attendance.timestamp >= time_threshold
            ).delete()
            
            db.commit()
            logger.info(f"🗑️ [WINDOW_RESET]: Reset duplicate lock for {uid} in {subject}")
            return True
        except Exception as e:
            logger.error(f"❌ [RESET_ERR]: {e}")
            db.rollback()
            return False

# Singleton instance for high-speed lifecycle management
duplicate_service = DuplicateDetectionService()