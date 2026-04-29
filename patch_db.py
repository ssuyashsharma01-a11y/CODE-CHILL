from backend.app.db.session import engine
from sqlalchemy import text
import os

# Project root ensure karne ke liye
print(f"📡 CONNECTING TO MATRIX DB: {os.path.abspath('trustmark_v6.db')}")

patch_queries = [
    "ALTER TABLE activities ADD COLUMN client_ip VARCHAR",
    "ALTER TABLE activities ADD COLUMN user_agent VARCHAR",
    "ALTER TABLE activities ADD COLUMN confidence_score FLOAT"
]

try:
    with engine.connect() as conn:
        for query in patch_queries:
            try:
                conn.execute(text(query))
                print(f"✅ SUCCESS: {query.split('ADD COLUMN ')[1]} added.")
            except Exception as e:
                # Agar column pehle se hai toh error ignore karega
                if "duplicate column name" in str(e).lower() or "already exists" in str(e).lower():
                    print(f"ℹ️ SKIP: {query.split('ADD COLUMN ')[1]} already exists in schema.")
                else:
                    print(f"⚠️ QUERY FAILED: {e}")
        
        conn.commit()
        print("\n✨ GLOBAL MATRIX PATCH COMPLETE: Dashboard connectivity synchronized!")
except Exception as e:
    print(f"❌ CRITICAL CONNECTION ERROR: {e}")
