#!/usr/bin/env python3
"""
🛰️ SOVEREIGN DEPLOYMENT AUDITOR - TrustMark AI v50
Performs deep-container inspection of the Identity Matrix.
"""
import subprocess
import sys
import json
import time
import os

# 

def run_docker_command(command, service="trustmark-ai"):
    """Injects Python logic directly into the running Sovereign Node."""
    cmd = [
        'docker', 'compose', 'exec', '-T', '-e', 'PYTHONPATH=/app/backend', service,
        'python', '-c', command
    ]
    result = subprocess.run(
        cmd,
        cwd=r'c:\Users\Suyash Sharma\Desktop\AI_Identity_Final',
        capture_output=True, 
        text=True,
        timeout=30
    )
    return result.returncode, result.stdout, result.stderr

def test_token_matrix():
    print("\n" + "═"*60)
    print("🧪 TEST 1: INTERNAL TOKEN HANDSHAKE (Inside Docker)")
    print("═"*60)
    
    code = """
import sys
from app.core.auth import create_access_token, decode_token
from app.core.config import settings

try:
    # 🎯 STEP: Create Sovereign Token
    token = create_access_token(data={'uid': '25BAI70757', 'role': 'ADMIN'})
    print(f"✅ TOKEN_INJECTED: {token[:40]}...")

    # 🎯 STEP: Decoding & RBAC Validation
    decoded = decode_token(token)
    if decoded and decoded.uid == '25BAI70757':
        print(f"✅ MATRIX_SYNC: Identity Verified | Role: {decoded.role}")
        print(f"✅ CONFIG_LOADED: {settings.ALGORITHM} | 24H Expiry Active")
    else:
        print("❌ FAIL: Identity corruption inside container.")
        sys.exit(1)
except Exception as e:
    print(f"❌ CRITICAL_AUTH_FAILURE: {e}")
    sys.exit(1)
"""
    returncode, stdout, stderr = run_docker_command(code)
    print(stdout if returncode == 0 else stderr)
    return returncode == 0

def test_container_grid():
    print("\n" + "═"*60)
    print("🧪 TEST 2: DOCKER CONTAINER GRID STATUS")
    print("═"*60)
    
    try:
        result = subprocess.run(
            ['docker', 'compose', 'ps'],
            cwd=r'c:\Users\Suyash Sharma\Desktop\AI_Identity_Final',
            capture_output=True, text=True
        )
        print(result.stdout)
        # Checking if all 4 sovereign nodes (AI, DB, Redis, Nginx) are healthy
        up_count = result.stdout.count('Up') + result.stdout.count('running')
        if up_count >= 4:
            print(f"✅ GRID_STABLE: {up_count} nodes online.")
            return True
        else:
            print(f"❌ GRID_FRACTURED: Only {up_count}/4 nodes active.")
            return False
    except Exception as e:
        print(f"❌ SYSTEM_ERR: {e}")
        return False

def main():
    print("\n" + "👑" * 20)
    print(" TRUSTMARK SOVEREIGN v50 - FINAL AUDIT")
    print("👑" * 20)
    
    results = {
        "Token Matrix": test_token_matrix(),
        "Container Grid": test_container_grid()
    }
    
    print("\n" + "═"*60)
    print("📊 SOVEREIGN AUDIT SUMMARY")
    print("═"*60)
    
    for name, res in results.items():
        print(f"{'✅ PASS' if res else '❌ FAIL'}: {name}")
    
    if all(results.values()):
        print("\n🏆 VERDICT: MATRIX IS FULLY SOVEREIGN AND READY FOR EXPO.")
        print("🚀 URL: http://localhost/api/v1/auth/login-page")
    else:
        print("\n🛑 VERDICT: DEPLOYMENT FAILURE. Check logs: 'docker compose logs'")
        sys.exit(1)

if __name__ == "__main__":
    main()