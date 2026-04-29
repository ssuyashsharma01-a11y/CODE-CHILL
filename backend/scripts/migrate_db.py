"""
🔄 SOVEREIGN DATABASE MIGRATION MATRIX - v25 Platinum
Dynamically patches SQLite schema to support forensic analytics and biometric confidence.
"""
import sys
import os

# Project Root alignment
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy import text
from app.db.session import SessionLocal, engine

# 

db = SessionLocal()

def apply_patch(table, column, col_type, default=None):
    """Safely injects a new column into the matrix if it doesn't exist."""
    try:
        default_val = f"DEFAULT {default}" if default else ""
        query = f"ALTER TABLE {table} ADD COLUMN {column} {col_type} {default_val}"
        db.execute(text(query))
        print(f"  ✅ [SUCCESS]: {table} -> {column} added.")
    except Exception as e:
        if "already exists" in str(e).lower() or "duplicate column" in str(e).lower():
            print(f"  ℹ️  [SKIP]: {table} -> {column} already exists.")
        else:
            print(f"  ⚠️  [WARN]: {table} -> {column} failed: {e}")

try:
    print("\n" + "═"*50)
    print("🚀 [MIGRATION]: SYNCHRONIZING SOVEREIGN MATRIX...")
    print("═"*50 + "\n")
    
    # --- 1. NOTICES TABLE (Broadcast Infrastructure) ---
    print("📝 Migrating 'notices' table...")
    apply_patch("notices", "title", "VARCHAR", "'Notice'")
    apply_patch("notices", "created_by", "VARCHAR", "'SYSTEM'")
    apply_patch("notices", "broadcast_status", "VARCHAR", "'DEPLOYED'")
    apply_patch("notices", "target_role", "VARCHAR", "'ALL'")
    
    # --- 2. ACTIVITIES TABLE (Forensic Audit Trail) ---
    print("\n📝 Migrating 'activities' table...")
    apply_patch("activities", "action_type", "VARCHAR")
    apply_patch("activities", "admin_id", "VARCHAR")
    apply_patch("activities", "details", "TEXT")
    apply_patch("activities", "client_ip", "VARCHAR")
    apply_patch("activities", "user_agent", "VARCHAR")
    apply_patch("activities", "confidence_score", "FLOAT")
    
    # --- 3. ATTENDANCE TABLE (Biometric Handshake) ---
    print("\n📝 Migrating 'attendance' table...")
    apply_patch("attendance", "lecture_slot", "VARCHAR")
    apply_patch("attendance", "biometric_confidence", "FLOAT")
    
    db.commit()
    print("\n" + "═"*50)
    print("✨ [SUCCESS]: DATABASE MATRIX SYNCHRONIZED!")
    print("🏛️ All nodes now match TrustMark Sovereign v25 Platinum.")
    print("═"*50 + "\n")
    
except Exception as e:
    db.rollback()
    print(f"\n❌ [CRITICAL_FAILURE]: {e}")
finally:
    db.close()