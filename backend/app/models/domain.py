from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Index, Time, Float, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.session import Base

# 

class User(Base):
    __tablename__ = "users"
    uid = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    password_hash = Column(String, nullable=True)
    encoding = Column(String, nullable=True) # High-precision 128D Vector (JSON String)
    role = Column(String, default="STUDENT", index=True) # STUDENT, TEACHER, ADMIN, CHIEF
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    logs = relationship("Attendance", back_populates="user", cascade="all, delete-orphan")
    broadcasts = relationship("BroadcastMessage", back_populates="recipient")
    
    __table_args__ = (
        Index('idx_user_role_created', 'role', 'created_at'),
    )

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String, ForeignKey("users.uid"), nullable=False, index=True)
    subject = Column(String, nullable=False, default="AI_IDENTITY_CORE", index=True)
    lecture_slot = Column(String, nullable=True)  # Morning, Lunch, Evening, Outside
    status = Column(String, nullable=False, default="VERIFIED", index=True) # VERIFIED, DL_MARKED, SPOOF_REJECTED
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    biometric_confidence = Column(Float, nullable=True) # Laplacian variance / Match distance
    anti_spoof = Column(Boolean, nullable=True, default=False, index=True)
    location = Column(String, nullable=True)
    
    user = relationship("User", back_populates="logs")
    
    __table_args__ = (
        Index('idx_attendance_uid_subject_timestamp', 'uid', 'subject', 'timestamp'),
        Index('idx_attendance_timestamp', 'timestamp'),
    )

class Activity(Base):
    """🔍 SOVEREIGN AUDIT TRAIL: Captures forensic metadata for the Identity Matrix."""
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, nullable=False)
    action_type = Column(String, nullable=True, index=True) # LOGIN, ENROLL, ATTENDANCE, SPOOF_DETECTED
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    user_id = Column(String, nullable=True, index=True)
    admin_id = Column(String, nullable=True) 
    details = Column(Text, nullable=True) # Raw JSON Metadata storage
    client_ip = Column(String, nullable=True, index=True)
    user_agent = Column(String, nullable=True)
    confidence_score = Column(Float, nullable=True)
    
    __table_args__ = (
        Index('idx_activity_timestamp_user', 'timestamp', 'user_id'),
        Index('idx_activity_type_timestamp', 'action_type', 'timestamp'),
    )

class Notice(Base):
    __tablename__ = "notices"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    is_urgent = Column(Boolean, default=False, index=True)
    created_by = Column(String, ForeignKey("users.uid"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    broadcast_status = Column(String, default="DEPLOYED", index=True) # QUEUED, DEPLOYED, ARCHIVED
    target_role = Column(String, default="ALL")
    
    messages = relationship("BroadcastMessage", back_populates="notice", cascade="all, delete-orphan")

class TimeTable(Base):
    __tablename__ = "time_tables"
    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, nullable=False, index=True)
    day_of_week = Column(Integer, nullable=False) # 0=Mon, 6=Sun
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    lecture_slot = Column(String, nullable=False) # Morning/Evening
    semester_cycle = Column(String, default="JAN_MAY")
    
    __table_args__ = (
        Index('idx_timetable_subject_day', 'subject', 'day_of_week'),
    )

class DutyLeave(Base):
    __tablename__ = "duty_leaves"
    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String, ForeignKey("users.uid"), nullable=False, index=True)
    subject = Column(String, nullable=False, index=True)
    date = Column(DateTime, nullable=False)
    reason = Column(Text, nullable=True)
    is_valid = Column(Boolean, default=True, index=True)
    semester_cycle = Column(String, nullable=False, default="JAN_MAY")

class BroadcastMessage(Base):
    __tablename__ = "broadcast_messages"
    id = Column(Integer, primary_key=True, index=True)
    notice_id = Column(Integer, ForeignKey("notices.id"), nullable=False)
    uid = Column(String, ForeignKey("users.uid"), nullable=False, index=True)
    is_read = Column(Boolean, default=False, index=True)
    read_at = Column(DateTime, nullable=True)
    
    notice = relationship("Notice", back_populates="messages")
    recipient = relationship("User", back_populates="broadcasts")