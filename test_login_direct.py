#!/usr/bin/env python3
"""
🔐 SOVEREIGN AUTH PROBE - TrustMark AI v50
Simulates the internal authentication handshake to verify Matrix credentials.
"""
import sys
import os
import bcrypt

# 

# 🎯 STEP 1: Absolute Path Injection
PROJECT_ROOT = r'c:\Users\Suyash Sharma\Desktop\AI_Identity_Final'
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'backend'))

from app.db.session import SessionLocal
from app.models.domain import User
from app.core.auth import create_access_token

def verify_identity(username: str, password: str):
    db = SessionLocal()
    print(f"\n📡 [PROBE]: Testing credentials for Node: {username}")
    
    try:
        # 1. Normalize UID
        target_uid = username.upper().strip()
        
        # 2. Database Lookup
        user = db.query(User).filter(User.uid == target_uid).first()
        if not user:
            print(f"❌ [DB_ERR]: Node {target_uid} not found in the Matrix.")
            return False
        
        print(f"✅ [NODE_FOUND]: Identity: {user.name} | Access Level: {user.role}")
        
        # 3. Cryptographic Verification
        try:
            # Cleaning the hash from potential quote corruption
            raw_hash = user.password_hash.strip()
            if raw_hash.startswith(("'", '"')) and raw_hash.endswith(("'", '"')):
                raw_hash = raw_hash[1:-1]
            
            stored_hash_bytes = raw_hash.encode('utf-8')
            
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash_bytes):
                print(f"✅ [SEC_PASS]: Cryptographic handshake successful.")
            else:
                print(f"❌ [SEC_FAIL]: Password mismatch for {target_uid}.")
                return False
        except Exception as e:
            print(f"❌ [CRYPTO_ERR]: Hash verification failed: {e}")
            return False
        
        # 4. Token Matrix Generation
        token = create_access_token(data={"uid": user.uid, "role": user.role})
        print(f"✅ [TOKEN_GEN]: Access key generated -> {token[:40]}...")
        return True

    finally:
        db.close()

def main():
    print("\n" + "═"*60)
    print(" 🕵️  TRUSTMARK SOVEREIGN v50 - AUTHENTICATION PROBE")
    print("═"*60)
    
    # Testing both critical nodes
    test_cases = [
        ("TEACHER01", "teach123"),
        ("25BAI70757", "trustmark_secure_2026") # Tera Admin account
    ]
    
    overall_success = True
    for uid, pwd in test_cases:
        if not verify_identity(uid, pwd):
            overall_success = False
            
    print("\n" + "═"*60)
    if overall_success:
        print("🏆 [VERDICT]: ALL IDENTITY NODES ARE SYNCED & SECURE!")
    else:
        print("🛑 [VERDICT]: AUTHENTICATION MISMATCH DETECTED. Re-run Seed scripts.")
    print("═"*60 + "\n")

if __name__ == "__main__":
    main()