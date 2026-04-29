#!/usr/bin/env python3
"""
🔐 SOVEREIGN AUTH DEBUGGER - TrustMark AI v50
Probes the database to verify Teacher node synchronization.
"""
import sys
import os
import bcrypt

# 

# 🎯 STEP 1: Absolute Path Injection
# Adjust this to where your backend actually sits
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

try:
    from app.db.session import SessionLocal
    from app.models.domain import User
except ImportError as e:
    print(f"❌ [IMPORT_ERR]: Matrix modules not found. Check sys.path. Error: {e}")
    sys.exit(1)

def run_debug():
    db = SessionLocal()
    target_uid = "TEACHER01"
    test_password = "teach123"

    print("\n" + "═"*60)
    print(f"📡 [DEBUG_PROBE]: VERIFYING IDENTITY NODE -> {target_uid}")
    print("═"*60)

    try:
        # 1. Fetch Node
        teacher = db.query(User).filter(User.uid == target_uid).first()
        if not teacher:
            print(f"❌ [DB_ERR]: Node '{target_uid}' is missing from the database.")
            return

        print(f"✅ [NODE_FOUND]: {teacher.name} | Role: {teacher.role}")
        print(f"📌 [HASH_PREVIEW]: {teacher.password_hash[:45]}...")

        # 2. Cryptographic Handshake
        print("\n🧪 [CRYPTO_TEST]: Validating password '{0}'...".format(test_password))
        
        try:
            # Cleaning the hash from potential string-literal artifacts (extra quotes)
            raw_hash = teacher.password_hash.strip()
            if raw_hash.startswith(("'", '"')) and raw_hash.endswith(("'", '"')):
                raw_hash = raw_hash[1:-1]
            
            stored_hash_bytes = raw_hash.encode('utf-8')
            password_bytes = test_password.encode('utf-8')

            # The actual Bcrypt check
            if bcrypt.checkpw(password_bytes, stored_hash_bytes):
                print("✅ [SEC_PASS]: Password matches the stored hash!")
                print("🚀 Matrix verdict: LOGIN WILL WORK.")
            else:
                print("❌ [SEC_FAIL]: Password mismatch.")
                print("💡 Tip: Try re-seeding the user with get_password_hash().")

        except Exception as e:
            print(f"❌ [CRYPTO_ERR]: Verification exploded: {e}")

    finally:
        db.close()
    print("═"*60 + "\n")

if __name__ == "__main__":
    run_debug()