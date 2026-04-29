import re
import logging
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import Optional, Dict, Any

# Adjust this import based on where your Activity model is actually located
# If it's in backend/app/models/domain.py, use:
from ..models.domain import Activity 

# Setup basic logging
logger = logging.getLogger("audit_service")

class AuditService:
    @staticmethod
    def _mask_sensitive_data(data: Any) -> Any:
        """Recursively mask sensitive identifiers."""
        if isinstance(data, str):
            # Masks 12-digit numbers
            return re.sub(r'\b\d{12}\b', "XXXXXXXXXXXX", data)
        if isinstance(data, dict):
            return {k: AuditService._mask_sensitive_data(v) for k, v in data.items()}
        return data

    @staticmethod
    def log_action(
        db: Session, 
        action: str, 
        user_id: Optional[str] = None, 
        details: Optional[Dict[str, Any]] = None
    ) -> Optional[Activity]:
        try:
            safe_details = AuditService._mask_sensitive_data(details) if details else None
            
            activity = Activity(
                action=action.upper(),
                user_id=user_id,
                details=safe_details,
                timestamp=datetime.now(timezone.utc)
            )
            
            db.add(activity)
            db.commit()
            db.refresh(activity)
            return activity
            
        except Exception as e:
            db.rollback()
            logger.error(f"AUDIT_LOG_FAILURE: {str(e)}")
            return None

    @staticmethod
    def get_audit_logs(db: Session, limit: int = 100, offset: int = 0, user_id: Optional[str] = None):
        # Using Activity here requires it to be imported correctly above
        query = db.query(Activity).order_by(Activity.timestamp.desc())
        if user_id:
            query = query.filter(Activity.user_id == user_id)
        return query.offset(offset).limit(limit).all()

# Singleton instance
audit_service = AuditService()