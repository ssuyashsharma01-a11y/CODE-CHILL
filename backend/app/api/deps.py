from typing import Optional
from fastapi import Depends, HTTPException, status, Cookie, Header
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from ..db.session import get_db
from ..core.config import settings
from ..models.domain import User
from ..core.auth import TokenData


# ============================================================================
# 🔐 TOKEN EXTRACTOR (Cookie + Header Support)
# ============================================================================

def get_token_from_request(
    access_token: Optional[str] = Cookie(None),
    authorization: Optional[str] = Header(None)
) -> str:
    """Extracts JWT from Matrix Cookie OR Authorization header"""
    token = None

    if access_token:
        token = access_token.replace("Bearer ", "")
    elif authorization:
        token = authorization.replace("Bearer ", "")
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Matrix Authentication Required"
        )
    return token


# ============================================================================
# 🛡️ CURRENT USER (JWT VALIDATION)
# ============================================================================

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(get_token_from_request)
) -> User:
    """Validates JWT and returns full DB user object (for operations needing profile data)"""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        uid: str = payload.get("uid")
        if uid is None:
            raise HTTPException(status_code=401, detail="Invalid identity payload")
            
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Neural Link failed: Token decode error"
        )

    # 🔍 Fetch user from DB
    user = db.query(User).filter(User.uid == uid).first()

    if not user:
        raise HTTPException(status_code=404, detail="Sovereign identity not found in registry")

    return user


# ============================================================================
# 🧠 TOKEN DATA ONLY (High-Performance / No DB Hit 🔥)
# ============================================================================

def get_token_data(
    token: str = Depends(get_token_from_request)
) -> TokenData:
    """Extracts identity data directly from JWT without hitting Database (Super Fast)"""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        uid: str = payload.get("uid")
        role: str = payload.get("role")
        
        if not uid or not role:
            raise HTTPException(status_code=401, detail="Incomplete identity data")
            
        return TokenData(uid=uid, role=role)

    except JWTError:
        raise HTTPException(status_code=401, detail="Token validation failed")


# ============================================================================
# 🔐 ROLE BASED ACCESS CONTROL (RBAC)
# ============================================================================

def require_admin(token_data: TokenData = Depends(get_token_data)) -> TokenData:
    """Fast check for Sovereign Root access"""
    if token_data.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sovereign Root access required"
        )
    return token_data


def require_teacher_admin(token_data: TokenData = Depends(get_token_data)) -> TokenData:
    """Fast check for Staff clearance"""
    if token_data.role not in ["ADMIN", "TEACHER"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Staff clearance required"
        )
    return token_data


def require_auth(token_data: TokenData = Depends(get_token_data)) -> TokenData:
    """Basic identity verification"""
    return token_data