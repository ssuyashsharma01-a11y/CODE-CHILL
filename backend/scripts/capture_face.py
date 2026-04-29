import cv2
import os
import base64
import requests
import json

# 

def capture_sovereign():
    # 🎯 STEP 1: Global Path Management
    SAVE_PATH = "backend/app/ai/training_data"
    os.makedirs(SAVE_PATH, exist_ok=True)

    # 🎯 STEP 2: Identity Metadata
    uid = input("🆔 Enter Student UID (e.g., 25BAI70757): ").upper().strip()
    name = input("👤 Enter Student Name: ").strip()
    
    if not uid or not name:
        print("❌ Error: UID and Name are mandatory for Matrix Synchronization!")
        return

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("❌ Camera not detected!")
        return

    print(f"\n--- TITANIUM IDENTITY INJECTION: {uid} ---")
    print("Action: Press 'SPACE' to Sync, 'ESC' to Abort.")

    while True:
        ret, frame = cam.read()
        if not ret: break
        
        # UI Overlay for Professional Look
        preview = cv2.flip(frame, 1)
        cv2.rectangle(preview, (160, 100), (480, 380), (0, 249, 255), 2) # Face Guide
        cv2.putText(preview, f"NODE: {uid}", (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 249, 255), 2)
        cv2.putText(preview, "ALIVE_SCAN: ACTIVE", (20, 70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        cv2.imshow("TrustMark AI - Sovereign Enrollment", preview)

        k = cv2.waitKey(1)
        if k == 27: # ESC
            print("🚫 ABORTED.")
            break
        elif k == 32: # SPACE
            # 1. Save Physical Copy
            img_name = f"{uid}.jpg"
            full_path = os.path.join(SAVE_PATH, img_name)
            cv2.imwrite(full_path, frame)
            
            # 2. Convert to Base64 for API Handshake
            _, buffer = cv2.imencode('.jpg', frame)
            img_base64 = base64.b64encode(buffer).decode('utf-8')

            # 3. AUTO-SYNC WITH DATABASE (API CALL)
            print(f"📡 Syncing {uid} with Sovereign Matrix...")
            try:
                # Assuming your server is running on 8000
                payload = {
                    "uid": uid,
                    "name": name,
                    "image_base64": img_base64
                }
                response = requests.post("http://127.0.0.1:8000/api/v1/admin/enroll", json=payload)
                
                if response.status_code == 200:
                    print(f"✅ [MATRIX_SYNC]: {uid} is now LIVE in Registry.")
                    # Trigger Memory Reload
                    requests.get("http://127.0.0.1:8000/api/v1/admin/reload-engine")
                else:
                    print(f"⚠️ [SYNC_FAIL]: Server returned {response.status_code}. Saved locally only.")
            except Exception as e:
                print(f"⚠️ [OFFLINE_MODE]: API not reachable. Encoding must be synced manually later.")
            
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_sovereign()