"""
Sovereign Identity Seed - TrustMark AI v25 Platinum
Establishes the root '25BAI70757' node with unified security.
"""
import sys
import os

# 🎯 Path injection: App ko root se detect karne ke liye
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.session import SessionLocal, engine, Base
from app.models.domain import User
from app.core.security import get_password_hash 

def run_fix():
    print("\n" + "═"*50)
    print("🚀 [MATRIX_FIX]: RE-INITIALIZING SOVEREIGN NODE...")
    print("═"*50)

    # 1. Ensure schema is ready
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 2. Official UID setup
        admin_uid = "25BAI70757"
        
        # Identity Check
        existing_node = db.query(User).filter(User.uid == admin_uid).first()
        
        if existing_node:
            print(f"ℹ️ NODE_ACTIVE: {admin_uid} already exists. Updating credentials...")
            existing_node.password_hash = get_password_hash("trustmark_secure_2026")
            existing_node.role = "ADMIN"
            existing_node.name = "Suyash Sharma (Chief)"
        else:
            print(f"⏳ INJECTING NEW NODE: {admin_uid}...")
            new_admin = User(
                uid=admin_uid,
                name="Suyash Sharma",
                password_hash=get_password_hash("trustmark_secure_2026"),
                role="ADMIN",
                encoding=None
            )
            db.add(new_admin)

        db.commit()
        print(f"✅ [SUCCESS]: Sovereign Node '{admin_uid}' synchronized.")
        print(f"🔑 ACCESS_KEY: trustmark_secure_2026")

    except Exception as e:
        db.rollback()
        print(f"❌ [CRITICAL_ERR]: {e}")
    finally:
        db.close()
    print("═"*50 + "\n")

if __name__ == "__main__":
    run_fix()