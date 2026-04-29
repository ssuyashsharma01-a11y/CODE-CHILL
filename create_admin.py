"""
🔐 SOVEREIGN ADMIN SEEDER (POSTGRES EDITION)
TrustMark AI v25 Platinum - Database Initialization Node
"""
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
import logging

# 

# --- CONFIGURATION ---
# Default 'postgres' user for initial setup
DATABASE_URL = "postgresql://postgres:platinum_password@localhost:5432/trustmark_db"

logger = logging.getLogger("TrustMark-PostgresSeed")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Admin(Base):
    """
    Sovereign Admin Entity - Root Authority for Postgres Matrix
    """
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

def seed_postgres_admin():
    """
    Initializes the 'admins' table and injects the root 'suyash_admin' node.
    """
    print("\n" + "═"*50)
    print("🚀 [POSTGRES_SYNC]: INITIALIZING AUTHORITY NODE...")
    print("═"*50)

    # 1. Create Schema
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # 2. Hashed Password (v25 Platinum Standard)
    # This hash matches your 'platinum123' or custom security layer
    hashed_pw = "$2b$12$gH01a5O0ibCAHlXmqNI8JeVXO1zDvTbcbnbKHI6JKEwkAhPv1EWi6"
    
    try:
        # Check if node already exists to prevent duplicate key errors
        existing_admin = db.query(Admin).filter(Admin.username == "suyash_admin").first()
        
        if not existing_admin:
            new_admin = Admin(
                username="suyash_admin", 
                hashed_password=hashed_pw
            )
            db.add(new_admin)
            db.commit()
            print("✅ [SUCCESS]: Root Admin 'suyash_admin' established.")
        else:
            print("ℹ️  [SKIP]: Authority node 'suyash_admin' already active.")
            
    except Exception as e:
        db.rollback()
        print(f"❌ [CRITICAL_ERR]: Connection failed: {e}")
        print("💡 Tip: Check if Docker Postgres is running and port 5432 is open.")
    finally:
        db.close()
    
    print("═"*50 + "\n")

if __name__ == "__main__":
    seed_postgres_admin()