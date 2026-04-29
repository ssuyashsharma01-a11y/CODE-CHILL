"""
JWT Authentication Core Module - TrustMark AI Platinum v25
Handles secure token lifecycle and cryptographic verification.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import logging

# Config file should have SECRET_KEY, ALGORITHM, and ACCESS_TOKEN_EXPIRE_MINUTES
from .config import settings

logger = logging.getLogger("TrustMark-Auth")

# Password context for secure bcrypt hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Token(BaseModel):
    """Sovereign access token schema"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenData(BaseModel):
    """Payload identity structure"""
    uid: Optional[str] = None
    role: Optional[str] = None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Validate raw input against stored hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate high-entropy bcrypt hash"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Generate JWT with identity claims and temporal constraints.
    """
    to_encode = data.copy()
    
    # Set expiration window
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    # Platinum Metadata: Ensuring sub claim matches UID for standards
    to_encode.update({
        "exp": expire,
        "sub": str(data.get("uid")),
        "iat": datetime.now(timezone.utc)
    })
    
    try:
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.SECRET_KEY, 
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    except Exception as e:
        logger.error(f"❌ [AUTH_ERR]: Token generation failed: {e}")
        raise

def decode_token(token: str) -> Optional[TokenData]:
    """
    Decode, decrypt, and validate session token integrity.
    """
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        
        # Priority mapping for identity
        uid: str = payload.get("uid") or payload.get("sub")
        role: str = payload.get("role")
        
        if uid is None:
            logger.warning("🛡️ [AUTH_WARN]: Token payload missing identity (uid/sub)")
            return None
            
        return TokenData(uid=uid, role=role)
    except JWTError as e:
        logger.error(f"🛡️ [AUTH_INVALID]: Token validation failed: {e}")
        return None