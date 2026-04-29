from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict
from datetime import datetime

# --- Student Enrollment: Admin Command ---
class UserEnroll(BaseModel):
    uid: str = Field(..., example="25BAI70757")
    name: str = Field(..., example="Suyash Sharma")
    image_base64: str = Field(..., description="The face image in Base64 format for 128-D encoding")

# --- Authentication Core ---
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600

class TokenData(BaseModel):
    uid: Optional[str] = None
    role: Optional[str] = None

# --- Attendance Handshake Feed ---
class AttendanceBase(BaseModel):
    subject: str
    status: str
    timestamp: datetime
    biometric_confidence: Optional[float] = None
    lecture_slot: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

# --- Identity Profile (For Dashboard Roster) ---
class UserResponse(BaseModel):
    uid: str
    name: str
    role: str
    created_at: Optional[datetime] = None
    
    # Platinum Meta: Dashboard UI analytics
    overall_attendance: float = 0.0
    total_records: int = 0
    # Dictionary of subject -> {attended, total_classes, attendance_percent}
    subject_attendance: Optional[Dict[str, Dict]] = None

    model_config = ConfigDict(from_attributes=True)

# --- Detailed Profile with Forensic Logs ---
class UserDetail(UserResponse):
    logs: List[AttendanceBase] = []

# --- Sovereign Broadcast (Notices) ---
class NoticeCreate(BaseModel):
    title: str
    content: str
    is_urgent: bool = False
    target_role: str = "ALL"

class NoticeResponse(BaseModel):
    id: int
    title: str
    content: str
    is_urgent: bool
    created_at: datetime
    broadcast_status: str

    model_config = ConfigDict(from_attributes=True)