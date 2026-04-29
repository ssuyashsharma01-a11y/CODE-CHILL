#!/usr/bin/env python3
"""
🔍 SOVEREIGN HEALTH MONITOR - TrustMark AI v25 Platinum
Forensic status checker for Dockerized Identity Matrix.
"""

import subprocess
import os
import sys

# 

def run_cmd(cmd):
    """Executes system commands with forensic output capture."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
        return (result.stdout or '') + (result.stderr or '')
    except Exception as e:
        return f"❌ System Command Error: {str(e)}"

def main():
    print("\n" + "═"*60)
    print(" 🔐 TRUSTMARK SOVEREIGN v25 PLATINUM - MATRIX HEALTH AUDIT")
    print("═"*60)
    
    # 🎯 1. DOCKER ORCHESTRATION CHECK
    print("\n📡 [NODE_STATUS]: Inspecting Container Grid...")
    print("-" * 60)
    output = run_cmd(['docker', 'compose', 'ps'])
    if "Up" in output:
        print(output)
        print("✅ GRID_STABILITY: Active")
    else:
        print(output)
        print("⚠️  GRID_STABILITY: Nodes are offline or initializing.")
    
    # 🎯 2. REAL-TIME AI CORE LOGS
    print("\n🧠 [AI_CORE_LOGS]: Inspecting Biometric Handshake (Last 15 lines)...")
    print("-" * 60)
    # Using 'trustmark-ai' as the service name from docker-compose
    logs = run_cmd(['docker', 'compose', 'logs', 'trustmark-ai', '--tail', '15'])
    if logs.strip():
        print(logs)
    else:
        print("ℹ️  LOG_EMPTY: AI Core hasn't broadcasted yet.")
    
    # 🎯 3. SOVEREIGN API HANDSHAKE
    print("\n📡 [API_HANDSHAKE]: Testing Endpoint Connectivity...")
    print("-" * 60)
    try:
        import requests
        # Testing the WhoAmI endpoint (requires Auth, so 401 is a success sign)
        try:
            resp = requests.get('http://localhost/api/v1/status', timeout=5)
            print(f"📡 Matrix Status Endpoint: {resp.status_code}")
            
            if resp.status_code == 200:
                data = resp.json()
                print(f"✅ CORE_ONLINE: Version {data.get('version')} | Engine: {data.get('engine')}")
            else:
                print(f"⚠️  UNEXPECTED_RESPONSE: {resp.status_code}")
        except requests.exceptions.ConnectionError:
            print("❌ CONNECTION_REFUSED: Matrix Node at localhost:80 is unreachable.")
            print("   (Check if Nginx container is running or Port 80 is occupied)")
    except ImportError:
        print("⚠️  TOOL_MISSING: 'requests' module not found. Run 'pip install requests'.")
    
    # 🎯 4. FORENSIC SUMMARY
    print("\n📝 [AUDIT_SUMMARY]")
    print("-" * 60)
    print("""
🚦 SYSTEM_SIGNALS:
   🟢 ALL 'UP' & Status 200 -> Matrix is Fully Sovereign.
   🟡 401 Unauthorized -> Security Layer is Active (GOOD).
   🔴 Connection Refused -> Wait for Docker Build or 'docker-compose up --build'.

🛠️  RECOVERY_COMMANDS:
   - View Live Logs: docker compose logs -f trustmark-ai
   - Hard Reset:     docker compose down -v && docker compose up -d --build
    """)
    print("═"*60 + "\n")

if __name__ == "__main__":
    main()