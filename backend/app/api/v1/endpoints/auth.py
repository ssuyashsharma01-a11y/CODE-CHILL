import bcrypt
import logging
from fastapi import APIRouter, Depends, HTTPException, Response, Cookie, Header, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
from typing import Optional

from ....db.session import get_db
from ....models.domain import User
from ....core.auth import create_access_token, TokenData, decode_token
from ....core.config import settings

router = APIRouter(tags=["authentication"])
logger = logging.getLogger("Auth-Sovereign")

# =========================
# 🔐 MATRIX LOGIN
# =========================
@router.post("/login")
async def login(
    response: Response,
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    uid = form_data.username.upper()
    user = db.query(User).filter(User.uid == uid).first()

    # 🛑 Identity Check
    if not user:
        logger.warning(f"❌ [AUTH_FAIL]: Identity {uid} not found.")
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid Matrix Credentials")

    # 🛡️ Password Verification
    try:
        if not bcrypt.checkpw(form_data.password.encode(), user.password_hash.encode()):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid Matrix Credentials")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Cryptographic Error")

    # 🧬 Generate Sovereign Token
    token = create_access_token({
        "uid": user.uid,
        "role": user.role
    })

    # Prepare Response
    res = JSONResponse({
        "status": "success",
        "role": user.role,
        "name": user.name,
        "redirect": "/api/v1/pages/index"
    })

    # 🍪 Secure Cookie Injection
    res.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        secure=False,      # ⚠️ Set TRUE in production (HTTPS)
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/"
    )

    logger.info(f"🔑 [AUTH_SUCCESS]: {user.uid} (Role: {user.role}) is now ONLINE.")
    return res

# =========================
# 🛡️ SESSION GUARD
# =========================
async def get_current_user(
    access_token: Optional[str] = Cookie(None),
    authorization: Optional[str] = Header(None)
) -> TokenData:
    token = None
    if access_token:
        token = access_token.replace("Bearer ", "")
    elif authorization:
        token = authorization.replace("Bearer ", "")

    if not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Neural Link Offline: Login Required")

    payload = decode_token(token)
    if not payload:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Session Corrupted: Please re-authenticate")

    return TokenData(uid=payload.get("uid"), role=payload.get("role"))

# =========================
# 🔐 RBAC (Role Checks)
# =========================
async def require_admin(user: TokenData = Depends(get_current_user)):
    if user.role != "ADMIN":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Sovereign Root Access Required")
    return user

async def require_teacher_admin(user: TokenData = Depends(get_current_user)):
    if user.role not in ["ADMIN", "TEACHER"]:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Staff Clearance Required")
    return user

# =========================
# 🚪 TERMINATE LINK (Logout)
# =========================
@router.post("/logout")
async def logout():
    res = JSONResponse({
        "status": "Terminated",
        "redirect": "/api/v1/auth/login-page"
    })
    res.delete_cookie("access_token", path="/")
    logger.info("🛑 [AUTH_TERMINATED]: Sovereign session ended.")
    return res

# =========================
# 👤 IDENTITY SYNC (WhoAmI)
# =========================
@router.get("/whoami")
async def whoami(
    user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.uid == user.uid).first()
    if not db_user:
        raise HTTPException(404, "Identity not in Registry")

    return {
        "uid": user.uid,
        "role": user.role,
        "name": db_user.name
    }

# =========================
# 🔑 UPDATE KEY (Change Password)
# =========================
@router.post("/change-password")
async def change_password(
    old_password: str,
    new_password: str,
    db: Session = Depends(get_db),
    user: TokenData = Depends(get_current_user)
):
    db_user = db.query(User).filter(User.uid == user.uid).first()

    if not bcrypt.checkpw(old_password.encode(), db_user.password_hash.encode()):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Validation Failed: Old password incorrect")

    # Hash and Store
    new_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
    db_user.password_hash = new_hash.decode()

    try:
        db.commit()
        return {"status": "success", "message": "Neural Key Updated"}
    except Exception:
        db.rollback()
        raise HTTPException(500, "Registry Sync Failed")