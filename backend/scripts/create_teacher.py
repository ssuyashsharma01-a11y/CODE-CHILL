import sys
import os

# 

# 1. FIX: Path logic taaki 'app' module mil jaye
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal, engine, Base
from app.models.domain import User
from app.core.security import get_password_hash # Using unified security

def seed_matrix_authority():
    """
    Sovereign Node Injection: Creates the initial Teacher/Admin accounts.
    """
    # Ensure tables exist before seeding
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if teacher already exists to prevent duplicates
        teacher = db.query(User).filter(User.uid == "TEACHER01").first()
        
        if not teacher:
            # 2. FIX: Unified Hashing (bcrypt through our security module)
            raw_password = "teach123"
            hashed_pwd = get_password_hash(raw_password)
            
            new_teacher = User(
                uid="TEACHER01",
                name="Prof. Suyash Sharma",
                password_hash=hashed_pwd,
                role="TEACHER" # Dashboard access level
            )
            
            db.add(new_teacher)
            db.commit()
            
            print("\n" + "═"*40)
            print("✅ SOVEREIGN NODE CREATED SUCCESSFULLY!")
            print(f"📌 IDENTITY: TEACHER01")
            print(f"📌 ACCESS_KEY: {raw_password}")
            print(f"📌 ROLE: TEACHER / ADMIN_PRIVILEGE")
            print("═"*40)
        else:
            print("ℹ️  NODE_EXISTS: TEACHER01 is already active in the Matrix.")
            
    except Exception as e:
        print(f"❌ CRITICAL_SEED_ERROR: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_matrix_authority()