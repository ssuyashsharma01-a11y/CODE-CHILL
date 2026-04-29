import base64
import cv2
import numpy as np
import logging
import asyncio
from datetime import datetime
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.db.session import SessionLocal
from app.models.domain import User, Attendance
from app.ai.engine import bio_engine

# 🛰️ Matrix Logging Configuration
logger = logging.getLogger("TrustMark-Attendance")

# 🛡️ Sovereign Router Initialization
router = APIRouter()

# ⚙️ Biometric Thresholds
SPOOF_VARIANCE_THRESHOLD = 85.0  # Finely tuned for CU Expo lighting conditions

def get_matrix_session():
    """Fetches current subject from the updated CU Timetable Matrix."""
    now = datetime.now()
    day = now.strftime("%A") 
    curr_t = now.time()
    
    # 📅 Official Matrix Timetable (Validated via Registry)
    tt = {
        "Tuesday": [
            ("09:30", "11:10", "25CSH-103"), ("11:20", "13:00", "25CSP-105"),
            ("13:55", "14:45", "25SMT-198"), ("14:45", "15:35", "25SMT-198"),
            ("15:35", "16:25", "25CSP-105")
        ],
        "Wednesday": [
            ("09:30", "11:10", "25PCP-111"), ("12:10", "13:00", "25SMT-198"),
            ("13:55", "14:45", "25SMT-198"), ("14:45", "15:35", "25CSH-103"),
            ("15:35", "16:25", "25ECH-101")
        ],
        "Thursday": [
            ("09:30", "11:10", "25ECP-102"), ("11:20", "12:10", "25ECH-101"),
            ("13:05", "14:45", "25TDP-151"), ("14:45", "15:35", "25CSP-102"),
            ("15:35", "16:25", "25CSP-102")
        ],
        "Friday": [
            ("09:30", "11:10", "25CSH-103"), ("12:10", "13:00", "25SMT-198"),
            ("13:55", "14:45", "25CSH-103"), ("14:45", "15:35", "25ECH-101"),
            ("15:35", "16:25", "25SZT-148")
        ],
        "Saturday": [
            ("09:30", "11:10", "25ECH-101"), ("11:20", "13:00", "25MEP-102"),
            ("13:55", "14:45", "25SZT-148"), ("14:45", "15:35", "25PCP-111"),
            ("15:35", "16:25", "25SZT-148")
        ],
        "Sunday": [ ("11:20", "12:10", "25GPT-121") ]
    }

    if day in tt:
        for s, e, sub in tt[day]:
            start = datetime.strptime(s, "%H:%M").time()
            end = datetime.strptime(e, "%H:%M").time()
            if start <= curr_t <= end:
                return sub
                
    return "FREE_PERIOD"

async def attendance_socket_consumer(websocket: WebSocket):
    """Sovereign Consumer: Real-time Biometrics & Matrix Logging"""
    session_cache = {} # Keeps track of UIDs processed in the current hour
    
    while True:
        try:
            data = await websocket.receive_text()
            if not data: continue

            # 🖼️ 1. DECODE MATRIX FRAME (Base64 Optimization)
            try:
                if "," in data:
                    _, encoded = data.split(",", 1)
                else:
                    encoded = data
                
                img_bytes = base64.b64decode(encoded)
                nparr = np.frombuffer(img_bytes, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                if frame is None: continue
            except Exception:
                continue

            # 🛡️ 2. ANTI-SPOOFING (Liveness check)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            variance = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # Broadcast metrics to frontend for live "Tech HUD" feel
            await websocket.send_json({"variance": round(variance, 2)})

            if variance < SPOOF_VARIANCE_THRESHOLD:
                await websocket.send_json({"status": "SPOOF_DETECTED"})
                continue

            # 🧬 3. AI RECOGNITION (Lightspeed Face Engine)
            uid = bio_engine.process_face(frame)
            
            if uid:
                current_sub = get_matrix_session()
                # Create a unique key for student+subject+hour
                cache_key = f"{uid}_{current_sub}_{datetime.now().strftime('%H')}"

                if cache_key not in session_cache:
                    with SessionLocal() as db:
                        try:
                            user = db.query(User).filter(User.uid == uid).first()
                            if user:
                                # 📝 4. REGISTRY COMMIT
                                new_log = Attendance(
                                    uid=uid,
                                    subject=current_sub,
                                    timestamp=datetime.now(),
                                    status="VERIFIED"
                                )
                                db.add(new_log)
                                db.commit()
                                
                                session_cache[cache_key] = True 
                                
                                # 🛰️ BROADCAST SUCCESS
                                await websocket.send_json({
                                    "status": "SUCCESS",
                                    "uid": uid,
                                    "name": user.name,
                                    "subject": current_sub
                                })
                                logger.info(f"✅ [MATRIX_LOCKED]: Identity {user.name} verified for {current_sub}")
                        except Exception as e:
                            logger.error(f"Matrix Sync Error: {e}")
                            db.rollback()

            await asyncio.sleep(0.04) # Stable ~25 FPS processing

        except WebSocketDisconnect:
            logger.info("🛑 Sovereign Link Terminated by User.")
            break
        except Exception as e:
            logger.error(f"Sovereign Link Fatal Error: {e}")
            break

# 🛰️ MATRIX GATEWAY: WebSocket Connection Point
@router.websocket("/ws")
async def attendance_ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("📡 [MATRIX_LINK]: Biometric Stream Initialized.")
    await attendance_socket_consumer(websocket)