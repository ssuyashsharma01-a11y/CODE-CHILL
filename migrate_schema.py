#!/usr/bin/env python3
import sqlite3
import os
import sys

# 🎯 STEP 1: Strict Path Resolution (The Sovereign Fix)
# Isse hum VS Code ko batayenge ki project root 'backend' hai
CURRENT_FILE_PATH = os.path.abspath(__file__)
BACKEND_ROOT = os.path.dirname(CURRENT_FILE_PATH) 

# Ensure backend root is the first priority in sys.path
if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

# 🎯 STEP 2: Absolute DB Path
DB_PATH = os.path.join(BACKEND_ROOT, "trustmark_v6.db")

print(f"\n" + "═"*60)
print(f"🔧 [MIGRATION]: Matrix syncing at {DB_PATH}")
print("═"*60)

try:
    # 🔌 SQLite Connection Handshake
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check current table architecture
    cursor.execute("PRAGMA table_info(activities)")
    columns = {row[1] for row in cursor.fetchall()}
    
    # 💉 Forensic Column Injection
    if 'client_ip' not in columns:
        cursor.execute("ALTER TABLE activities ADD COLUMN client_ip VARCHAR")
        print("✅ NODE_SYNC: Added client_ip")
    if 'user_agent' not in columns:
        cursor.execute("ALTER TABLE activities ADD COLUMN user_agent VARCHAR")
        print("✅ NODE_SYNC: Added user_agent")
    if 'confidence_score' not in columns:
        cursor.execute("ALTER TABLE activities ADD COLUMN confidence_score FLOAT")
        print("✅ NODE_SYNC: Added confidence_score")
        
    conn.commit()
    conn.close()
    print("\n✨ [SUCCESS]: Matrix Schema is now Platinum Compliant.")

except Exception as e:
    print(f"⚠️  [SQL_RETRY]: Local SQL failed. Attempting SQLAlchemy Handshake...")
    # 🎯 STEP 3: Fallback using the app module
    try:
        from app.db.session import engine, Base
        Base.metadata.create_all(bind=engine)
        print("🔨 [FALLBACK]: Reconstructed using app models.")
    except Exception as final_err:
        print(f"❌ [FATAL]: Identity Matrix Sync Failed: {final_err}")

print("═"*60 + "\n")