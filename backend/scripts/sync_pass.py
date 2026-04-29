"""
🧬 SOVEREIGN FACE SYNC - TRUSTMARK AI v25 PLATINUM
Performs full-stack identity injection: Credentials + Biometric Encodings.
"""
import os
import sys
import json
import numpy as np

# 

# Path alignment to ensure 'app' discovery
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.session import SessionLocal, engine, Base
from app.models.domain import User
from app.core.security import get_password_hash

# Dynamic Import for AI features
try:
    import face_recognition
    FACE_AI_AVAILABLE = True
except ImportError:
    FACE_AI_AVAILABLE = False
    print("⚠️ [WARN]: face_recognition not found. Skipping biometric sync.")

def sync_full_identity():
    # Force schema creation
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    admin_uid = "25BAI70757"
    raw_pass = "trustmark_secure_2026"
    admin_photo = f"backend/app/ai/training_data/{admin_uid}.jpg"

    print("\n" + "═"*50)
    print(f"🚀 [IDENTITY_SYNC]: PRIMING SOVEREIGN NODE {admin_uid}")
    print("═"*50)

    try:
        user = db.query(User).filter(User.uid == admin_uid).first()
        
        # 1. GENERATE BIOMETRIC ENCODING
        encoding_str = None
        if FACE_AI_AVAILABLE and os.path.exists(admin_photo):
            print(f"🧬 [BIO_SCAN]: Processing photo -> {admin_photo}")
            img = face_recognition.load_image_file(admin_photo)
            encodings = face_recognition.face_encodings(img)
            
            if encodings:
                # Convert numpy array to JSON string for DB storage
                encoding_str = json.dumps(encodings[0].tolist())
                print("✅ [BIO_SYNC]: 128-D Vector injected into Matrix.")
            else:
                print("⚠️ [BIO_ERR]: No face detected in photo.")
        else:
            print("ℹ️ [BIO_SKIP]: Photo missing or AI libs offline.")

        # 2. SYNC CREDENTIALS & METADATA
        hashed_pwd = get_password_hash(raw_pass)
        
        if user:
            print(f"⏳ [SYNC]: Updating existing Node...")
            user.name = "Suyash Sharma (Chief)"
            user.password_hash = hashed_pwd
            user.role = "ADMIN"
            if encoding_str:
                user.encoding = encoding_str
        else:
            print(f"✨ [SYNC]: Injecting NEW Sovereign Node...")
            user = User(
                uid=admin_uid,
                name="Suyash Sharma",
                password_hash=hashed_pwd,
                role="ADMIN",
                encoding=encoding_str
            )
            db.add(user)

        db.commit()
        print("\n" + "═"*50)
        print(f"✅ [SUCCESS]: Sovereign Identity fully synchronized!")
        print(f"👤 NAME: {user.name}")
        print(f"🔑 PWD: {raw_pass}")
        print(f"🧬 BIO: {'LINKED' if user.encoding else 'NOT_LINKED'}")
        print("═"*50 + "\n")

    except Exception as e:
        db.rollback()
        print(f"❌ [CRITICAL_SYNC_FAIL]: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    sync_full_identity()