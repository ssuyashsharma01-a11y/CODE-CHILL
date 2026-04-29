import cv2
import face_recognition
import numpy as np
import logging
import time
from threading import Lock
from datetime import datetime, timedelta
from app.models.domain import Attendance, User

logger = logging.getLogger("TrustMark-Engine")

# 🧬 Global Engine Instance
class SovereignEngine:
    def __init__(self):
        self.known_encodings = []
        self.known_uids = []
        self.lock = Lock()
        self.is_active = True

    def load_ai_memory(self, db):
        """🧠 Syncs Enrolled Faces from Database to RAM"""
        with self.lock:
            logger.info("ENGINE: Loading identities into RAM...")
            # Assuming your User model has 'uid' and 'face_encoding' (as a list or blob)
            users = db.query(User).filter(User.face_encoding != None).all()
            
            self.known_encodings = [np.array(u.face_encoding) for u in users]
            self.known_uids = [u.uid for u in users]
            
            logger.info(f"✅ AI_MEMORY: {len(self.known_uids)} Identities Synchronized.")

    def process_face(self, frame):
        """🏎️ Light-Speed Face Matching (50% Optimization)"""
        if frame is None or not self.known_encodings:
            return None

        try:
            # 🏁 Resize for 4x faster processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            # 🔍 Detect and Encode
            face_locations = face_recognition.face_locations(rgb_frame)
            if not face_locations:
                return None

            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for face_encoding in face_encodings:
                # 🎯 Check distance against known identities
                distances = face_recognition.face_distance(self.known_encodings, face_encoding)
                if len(distances) == 0:
                    continue

                best_match_idx = np.argmin(distances)

                # 🛡️ Tolerance 0.5 for High Security Presentation
                if distances[best_match_idx] < 0.5:
                    return self.known_uids[best_match_idx]

            return None
        except Exception as e:
            logger.error(f"❌ PROCESS_ERROR: {e}")
            return None

    def inject_bulk_dl(self, db, uid, start_date, end_date, subject="SOVEREIGN_DL"):
        """🎓 Bulk Duty Leave Engine (1hr to 3 Months)"""
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            
            delta = end - start
            added_count = 0

            for i in range(delta.days + 1):
                current_day = start + timedelta(days=i)
                
                # 🚫 Skip Sundays (Matrix Standard)
                if current_day.weekday() == 6:
                    continue

                # Create Attendance Entry
                new_entry = Attendance(
                    uid=uid,
                    subject=subject,
                    timestamp=current_day.replace(hour=9, minute=0, second=0), # Standard shift
                    status="VERIFIED_DL",
                    lecture_slot="BULK_INJECTED"
                )
                db.add(new_entry)
                added_count += 1

            db.commit()
            logger.info(f"✅ BULK_DL: {added_count} records injected for UID {uid}")
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"❌ BULK_DL_FAIL: {e}")
            return False

    def get_history(self, db, uid=None, limit=50):
        """📜 Attendance History Fetcher"""
        query = db.query(Attendance)
        if uid:
            query = query.filter(Attendance.uid == uid)
        
        logs = query.order_by(Attendance.timestamp.desc()).limit(limit).all()
        return [
            {
                "uid": l.uid,
                "timestamp": l.timestamp.isoformat(),
                "subject": l.subject,
                "status": l.status
            } for l in logs
        ]

# 🧬 Singleton for the entire app
bio_engine = SovereignEngine()