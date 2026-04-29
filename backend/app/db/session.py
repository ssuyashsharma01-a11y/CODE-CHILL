"""
Sovereign Database Session Manager - TrustMark AI Platinum
Handles thread-safe connections and absolute path synchronization.
"""
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Setup logger
logger = logging.getLogger("TrustMark-Database")

# ✅ MASTER PATH CALIBRATION (No Ghost Databases)
# Docker environment check
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) # app/db/
APP_DIR = os.path.dirname(CURRENT_DIR) # app/
BACKEND_DIR = os.path.dirname(APP_DIR) # backend/
PROJECT_ROOT = os.path.dirname(BACKEND_DIR) # Final Project Folder

# DB Path configuration
DB_PATH = os.path.join(PROJECT_ROOT, "trustmark_v6.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

print(f"📡 [DATABASE_CONNECT]: Matrix synchronized at -> {DB_PATH}")

# ✅ ENGINE OPTIMIZATION
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}, # Critical for multi-threaded FastAPI
    pool_pre_ping=True # Health check before using a connection
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    """Sovereign Schema Declarative Base"""
    pass

# --- 🚀 THE MATRIX SYNC FUNCTION ---
def init_db_matrix():
    """
    Called by main.py to ensure all Matrix tables exist.
    Fixes the relative import issue with models.
    """
    try:
        # Relative import within the app structure
        from ..models import domain
        print("🔨 [DATABASE]: Synchronizing Matrix Tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ [DATABASE]: Matrix Sync Complete.")
    except Exception as e:
        print(f"❌ [DATABASE_ERR]: Sync Failed: {e}")

def get_db():
    """Context Manager for Database Transactions"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()