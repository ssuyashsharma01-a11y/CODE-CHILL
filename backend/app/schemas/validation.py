import re
from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator

# --- 🏷️ ENUMS ---
class SemesterCycle(str, Enum):
    JAN_MAY = "JAN_MAY"
    JUL_NOV = "JUL_NOV"

class UserRole(str, Enum):
    ALL = "ALL"
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"
    ADMIN = "ADMIN"

class SubjectMatrix(str, Enum):
    AI_CORE = "AI_IDENTITY_CORE"
    CRYPTO = "CRYPTOGRAPHY"
    BLOCKCHAIN = "BLOCKCHAIN"
    DATA_SCIENCE = "DATA_SCIENCE"
    ML_ENG = "ML_ENGINEERING"
    CYBER = "CYBERSECURITY"
    CLOUD = "CLOUD_ARCHITECTURE"
    DEVOPS = "DEVOPS"

# --- 🛠️ BASE MIXIN ---
class AcademicBase(BaseModel):
    model_config = {"from_attributes": True, "use_enum_values": True}

    @field_validator('uid', 'subject', check_fields=False)
    @classmethod
    def force_uppercase(cls, v: str):
        return v.upper() if isinstance(v, str) else v

# --- 👤 USER SCHEMAS ---
class UserBase(AcademicBase):
    uid: str = Field(..., min_length=3, max_length=50)
    name: str = Field(..., min_length=2, max_length=100)

class UserEnroll(UserBase):
    face_encoding: str = Field(..., description="Base64 capture from frontend")
    role: UserRole = UserRole.STUDENT

class UserLogin(BaseModel):
    uid: str
    password: str

# --- 📢 NOTICE SCHEMAS ---
class NoticeCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    content: str = Field(..., min_length=5, max_length=1000)
    is_urgent: bool = False
    target_role: UserRole = UserRole.ALL

class NoticeResponse(NoticeCreate):
    id: int
    created_by: str
    created_at: datetime
    broadcast_status: str = "ACTIVE"
    model_config = {"from_attributes": True}

# --- 📅 TIMETABLE SCHEMAS ---
class TimeTableCreate(AcademicBase):
    subject: SubjectMatrix
    day_of_week: int = Field(..., ge=0, le=6)
    start_time: str
    end_time: str
    lecture_number: int
    semester_cycle: SemesterCycle = SemesterCycle.JAN_MAY

class TimeTableResponse(TimeTableCreate):
    id: int
    lecture_slot: Optional[str] = None
    model_config = {"from_attributes": True}

# --- 🏥 DUTY LEAVE SCHEMAS ---
class DutyLeaveRequest(AcademicBase):
    uid: str
    subject: SubjectMatrix
    date: str
    reason: str
    semester_cycle: SemesterCycle = SemesterCycle.JAN_MAY

class DutyLeaveResponse(DutyLeaveRequest):
    id: int
    granted_by: Optional[str] = None
    is_valid: bool = False
    created_at: datetime
    model_config = {"from_attributes": True}

# --- 📊 ATTENDANCE & AUTH ---
class AttendanceCreate(AcademicBase):
    uid: str
    subject: SubjectMatrix = SubjectMatrix.AI_CORE

class Token(BaseModel):
    access_token: str
    token_type: str

class ActivityLogResponse(BaseModel):
    id: int
    action: str
    timestamp: datetime
    user_id: Optional[str]
    details: Optional[str]
    model_config = {"from_attributes": True}