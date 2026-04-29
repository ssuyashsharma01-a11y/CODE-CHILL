"""
Sovereign Admin Seeding Script - TrustMark AI Platinum v25
Initializes the root authority node for the Identity Matrix.
"""
import sys
import os

# 

# 🎯 STEP 1: Absolute Path Synchronization
# Ensures 'app' is recognized regardless of current terminal directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal, engine, Base, init_db_matrix
from app.models.domain import User
from app.core.security import get_password_hash

def seed_root_authority():
    """
    Injects the primary Admin Node into the database schema.
    """
    print("\n" + "═"*50)
    print("🚀 [MATRIX_SEED]: INITIALIZING SOVEREIGN AUTHORITY...")
    print("═"*50)

    # 🎯 STEP 2: Database Table Handshake
    # Verification logic from our updated session.py
    init_db_matrix()
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # 🎯 STEP 3: Identity Collision Check
        # Checking for 'admin' and 'TEACHER01'
        admin_node = db.query(User).filter(User.uid == "admin").first()
        
        if not admin_node:
            # Creating Root Admin
            new_admin = User(
                uid="admin",
                name="Suyash Sharma",
                password_hash=get_password_hash("platinum123"),
                role="ADMIN" # Explicit privilege level
            )
            db.add(new_admin)
            
            # Optional: Add a second testing node
            test_teacher = db.query(User).filter(User.uid == "TEACHER01").first()
            if not test_teacher:
                db.add(User(
                    uid="TEACHER01",
                    name="Sovereign Proctor",
                    password_hash=get_password_hash("teach123"),
                    role="TEACHER"
                ))

            db.commit()
            print("✅ [SUCCESS]: Root Authority Synced.")
            print("🏛️  NODE_ID: admin")
            print("🔑 ACCESS_KEY: platinum123")
            print("🛡️  PRIVILEGE: SOVEREIGN_ADMIN")
        else:
            print("ℹ️  [NODE_ACTIVE]: Admin authority already exists in Matrix.")
            
    except Exception as e:
        print(f"❌ [SEED_CRITICAL]: Synchronization failed: {e}")
        db.rollback()
    finally:
        db.close()
    print("═"*50 + "\n")

if __name__ == "__main__":
    seed_root_authority()