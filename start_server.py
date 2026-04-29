#!/usr/bin/env python3
"""
🚀 SOVEREIGN STARTUP ENGINE - TrustMark AI v50
Automated Port Validation & Matrix Deployment Script
"""
import subprocess
import sys
import time
import socket
import os

# --- 🎯 GLOBAL IDENTITY CONFIG ---
PROJECT_ROOT = r"c:\Users\Suyash Sharma\Desktop\AI_Identity_Final"
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")

def is_server_running():
    """Forensic check to see if port 8000 is occupied."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', 8000))
        sock.close()
        return result == 0
    except:
        return False

def launch_matrix():
    print("\n" + "═"*60)
    print(" 🔐 TRUSTMARK SOVEREIGN v50 - SYSTEM INITIALIZATION")
    print("═"*60)

    # 1. Port Conflict Guard
    if is_server_running():
        print("⚠️  [CONFLICT]: Matrix node already active on localhost:8000")
        print("💡 [ACTION]: Terminate existing process or use a different port.")
        sys.exit(0)

    print("📡 [STATUS]: Priming Biometric Pipeline...")
    
    # 2. Start Uvicorn Matrix
    # --reload is essential for development at CU Expo
    try:
        proc = subprocess.Popen(
            [
                sys.executable, "-m", "uvicorn", 
                "app.main:app", 
                "--host", "0.0.0.0", 
                "--port", "8000",
                "--reload" # Auto-sync changes during live demo
            ],
            cwd=BACKEND_DIR,
            env=os.environ.copy() # Keeps your virtualenv paths intact
        )

        # 3. Verification Handshake
        print("⏳ [WAIT]: Booting Sovereign AI Core...")
        time.sleep(3)

        if is_server_running():
            print("\n" + "═"*60)
            print(" ✅ [SUCCESS]: MATRIX IS LIVE AT http://localhost:8000")
            print(" 🛡️  LOGS: Streaming below...")
            print("═"*60 + "\n")
            
            # Keep the script alive so it streams logs to terminal
            proc.wait()
        else:
            print("❌ [FATAL]: Identity Matrix failed to boot. Check Python dependencies.")
            
    except KeyboardInterrupt:
        print("\n\n🛑 [SHUTDOWN]: Sovereign Core deactivated.")
    except Exception as e:
        print(f"❌ [CRITICAL_ERR]: {e}")

if __name__ == "__main__":
    launch_matrix()