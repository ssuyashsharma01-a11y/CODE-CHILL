"""Services module - Business logic layer"""

from .email_service import email_service, EmailService
from .audit_service import audit_service, AuditService
from .duplicate_detection import duplicate_service, DuplicateDetectionService

__all__ = ["email_service", "audit_service", "duplicate_service"]
