"""
Sovereign Admin & CU Schedule Seeding Script - TrustMark AI Platinum v25
Initializes the root authority node and the extracted CU Timetable.
"""
import sys
import os

# 🎯 STEP 1: Absolute Path Synchronization
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal, engine, Base, init_db_matrix
from app.models.domain import User, TimeTable 
from app.core.security import get_password_hash

def seed_root_authority():
    print("\n" + "═"*50)
    print("🚀 [MATRIX_SEED]: INITIALIZING SOVEREIGN AUTHORITY...")
    print("═"*50)

    init_db_matrix()
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # --- PART A: IDENTITY SEEDING ---
        admin_node = db.query(User).filter(User.uid == "admin").first()
        if not admin_node:
            db.add(User(
                uid="admin",
                name="Suyash Sharma",
                password_hash=get_password_hash("platinum123"),
                role="ADMIN"
            ))
            print("✅ [SUCCESS]: Root Admin Synced.")

        # --- PART B: CU TIME TABLE SEEDING (Extracted from Image) ---
        print("📅 [SEEDING]: Syncing CU Timetable...")
        
        cu_schedule = [
            # TUESDAY
            {"day": "Tue", "time": "09:30 - 11:10 AM", "subject": "25CSH-103", "instructor": "Pawandeep Kaur", "room": "Block-C1-611"},
            {"day": "Tue", "time": "11:20 - 01:00 PM", "subject": "25CSP-105", "instructor": "Jaswinder Kaur", "room": "Block-C1-303"},
            {"day": "Tue", "time": "01:55 - 02:45 PM", "subject": "25SMT-198", "instructor": "Amit Kumar", "room": "Block-C1-715"},
            {"day": "Tue", "time": "02:45 - 03:35 PM", "subject": "25SMT-198", "instructor": "Amit Kumar", "room": "Block-C1-704"},
            {"day": "Tue", "time": "03:35 - 04:25 PM", "subject": "25CSP-105", "instructor": "Jaswinder Kaur", "room": "Block-C1-704"},
            
            # WEDNESDAY
            {"day": "Wed", "time": "09:30 - 11:10 AM", "subject": "25PCP-111", "instructor": "Jaspal Singh Dhindsa", "room": "Block-C1-504"},
            {"day": "Wed", "time": "12:10 - 01:00 PM", "subject": "25SMT-198", "instructor": "Amit Kumar", "room": "Block-C1-616-A"},
            {"day": "Wed", "time": "01:55 - 02:45 PM", "subject": "25SMT-198", "instructor": "Amit Kumar", "room": "Block-C1-704"},
            {"day": "Wed", "time": "02:45 - 03:35 PM", "subject": "25CSH-103", "instructor": "Pawandeep Kaur", "room": "Block-C1-704"},
            {"day": "Wed", "time": "03:35 - 04:25 PM", "subject": "25ECH-101", "instructor": "Sachin", "room": "Block-C1-704"},

            # THURSDAY
            {"day": "Thu", "time": "09:30 - 11:10 AM", "subject": "25ECP-102", "instructor": "Sudhir Kumar", "room": "Block-C1-702"},
            {"day": "Thu", "time": "11:20 - 12:10 PM", "subject": "25ECH-101", "instructor": "Sachin", "room": "Block-C1-412"},
            {"day": "Thu", "time": "01:05 - 02:45 PM", "subject": "25TDP-151", "instructor": "Nandini Kaushal", "room": "Block-C1-604"},
            {"day": "Thu", "time": "02:45 - 04:25 PM", "subject": "25CSP-102", "instructor": "Dilpreet Singh", "room": "Block-C1-604"},

            # FRIDAY
            {"day": "Fri", "time": "09:30 - 11:10 AM", "subject": "25CSH-103", "instructor": "Pawandeep Kaur", "room": "Block-C1-511"},
            {"day": "Fri", "time": "12:10 - 01:00 PM", "subject": "25SMT-198", "instructor": "Amit Kumar", "room": "Block-C1-715-A"},
            {"day": "Fri", "time": "01:55 - 02:45 PM", "subject": "25CSH-103", "instructor": "Pawandeep Kaur", "room": "Block-C1-715"},
            {"day": "Fri", "time": "02:45 - 03:35 PM", "subject": "25ECH-101", "instructor": "Sachin", "room": "Block-C1-715"},
            {"day": "Fri", "time": "03:35 - 04:25 PM", "subject": "25SZT-148", "instructor": "Shubham", "room": "Block-C1-715"},

            # SATURDAY
            {"day": "Sat", "time": "09:30 - 11:10 AM", "subject": "25ECH-101", "instructor": "Sachin", "room": "Block-C1-414"},
            {"day": "Sat", "time": "11:20 - 01:00 PM", "subject": "25MEP-102", "instructor": "Paras Khullar", "room": "Block-C1-416"},
            {"day": "Sat", "time": "01:55 - 02:45 PM", "subject": "25SZT-148", "instructor": "Shubham", "room": "Block-C1-413"},
            {"day": "Sat", "time": "02:45 - 03:35 PM", "subject": "25PCP-111", "instructor": "Jaspal Singh Dhindsa", "room": "Block-C1-403"},
            {"day": "Sat", "time": "03:35 - 04:25 PM", "subject": "25SZT-148", "instructor": "Shubham", "room": "Block-C1-714"},

            # SUNDAY
            {"day": "Sun", "time": "11:20 - 12:10 PM", "subject": "25GPT-121", "instructor": "All", "room": "Block-C1-605"}
        ]

        for entry in cu_schedule:
            exists = db.query(TimeTable).filter_by(day=entry['day'], time=entry['time'], subject=entry['subject']).first()
            if not exists:
                db.add(TimeTable(**entry))

        db.commit()
        print("✅ [SUCCESS]: Matrix Timetable Fully Synced.")
            
    except Exception as e:
        print(f"❌ [SEED_CRITICAL]: Synchronization failed: {e}")
        db.rollback()
    finally:
        db.close()
    print("═"*50 + "\n")

if __name__ == "__main__":
    seed_root_authority()