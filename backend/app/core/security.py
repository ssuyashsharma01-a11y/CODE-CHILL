"""
Sovereign Security Module - TrustMark AI Platinum v25
Standardized Cryptography and JWT Governance.
"""
from datetime import datetime, timedelta, timezone
from typing import Any, Union, Optional, Dict
from jose import jwt
from passlib.context import CryptContext
from .config import settings
import logging

logger = logging.getLogger("TrustMark-Security")

# High-Entropy Password Context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(
    subject: Union[str, Any], 
    role: str = "student", 
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Creates a signed JWT with standardized Claims.
    Subject is typically the User UID.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    # Platinum Standard Claims
    # sub: Subject (UID), role: Access Level, iat: Issued At
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "uid": str(subject), # Redundancy for older frontend components
        "role": role,
        "iat": datetime.now(timezone.utc)
    }
    
    try:
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.SECRET_KEY, 
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    except Exception as e:
        logger.error(f"❌ [SECURITY_ERR]: Token signing failed: {e}")
        raise

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies identity via bcrypt hash comparison."""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    """Generates a secure cryptographic hash for storage."""
    return pwd_context.hash(password)

def validate_token_structure(token: str) -> bool:
    """Fast check to see if a token is even readable before DB hit."""
    try:
        jwt.get_unverified_claims(token)
        return True
    except Exception:
        return False