#!/usr/bin/env python3
"""
🚀 SOVEREIGN IGNITION NODE - TrustMark AI v25 Platinum
Launches the Biometric Matrix with optimized runtime parameters.
"""
import sys
import os
import subprocess
import logging

# 

# --- 🎯 CONFIGURATION ---
PROJECT_ROOT = r'c:\Users\Suyash Sharma\Desktop\AI_Identity_Final'
# Path injection for internal modules
sys.path.append(os.path.join(PROJECT_ROOT, 'backend'))

def launch_matrix():
    # Suppression of face_recognition warnings
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
    
    print("\n" + "═"*60)
    print(" 🔥 TRUSTMARK SOVEREIGN v25 PLATINUM - SYSTEM IGNITION")
    print(f" 📍 PROJECT_ROOT: {PROJECT_ROOT}")
    print("═"*60)

    try:
        os.chdir(PROJECT_ROOT)
        
        # --- 🚦 EXECUTING UVICORN ---
        # --reload: Auto-restarts server on code changes
        # --app-dir: Ensures backend structure is respected
        subprocess.run([
            sys.executable, '-m', 'uvicorn',
            'app.main:app', # Simplified path thanks to --app-dir
            '--host', '0.0.0.0',
            '--port', '8000',
            '--reload',
            '--app-dir', 'backend'
        ])
        
    except KeyboardInterrupt:
        print("\n\n🛑 [SYSTEM_SHUTDOWN]: Matrix deactivated gracefully.")
    except Exception as e:
        print(f"\n❌ [IGNITION_FAIL]: {e}")

if __name__ == "__main__":
    launch_matrix()