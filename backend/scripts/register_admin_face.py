import face_recognition
import json
import sys
import os
import numpy as np

# Ensure backend directory is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from app.db.session import SessionLocal
    from app.models.domain import User
except ImportError:
    print("❌ [PATH ERROR]: Ensure you are running from the backend root!")
    sys.exit()

def register_biometrics(uid: str, img_path: str):
    db = SessionLocal()
    print(f"⏳ [SYSTEM]: Analyzing Biometric Nodes for UID: {uid}...")
    
    if not os.path.exists(img_path):
        print(f"❌ [ERROR]: File {img_path} not found.")
        return

    try:
        # Load and encode
        image = face_recognition.load_image_file(img_path)
        
        # Increase jitters for better registration quality
        encodings = face_recognition.face_encodings(image, num_jitters=10)

        if not encodings:
            print("❌ [ERROR]: No face detected. Check lighting/alignment.")
            return
        
        if len(encodings) > 1:
            print("⚠️ [WARNING]: Multiple faces detected. Using the most prominent one.")

        # Serialize
        encoding_json = json.dumps(encodings[0].tolist())

        # DB Handshake
        user = db.query(User).filter(User.uid == uid).first()
        
        if user:
            user.encoding = encoding_json
            db.commit()
            print(f"✅ [SUCCESS]: Identity {user.name} ({uid}) Synchronized!")
        else:
            print(f"❌ [ERROR]: UID {uid} not found in DB.")

    except Exception as e:
        print(f"❌ [CRITICAL]: Failure: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    register_biometrics(uid="25BAI70757", img_path="suyash.jpg")