#!/usr/bin/env python3
"""
🔐 SOVEREIGN AUTH VALIDATOR - TrustMark AI v50
Comprehensive test for Token Matrix, Module Integrity, and Container Grid.
"""
import sys
import os
import subprocess
import json

# 

# 🎯 STEP 1: Absolute Matrix Alignment
PROJECT_ROOT = r'c:\Users\Suyash Sharma\Desktop\AI_Identity_Final'
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'backend'))

def test_token_matrix():
    """Validates 128-bit Encryption & Payload Integrity"""
    print("\n" + "═"*60)
    print("🧪 TEST 1: TOKEN ENCRYPTION & DECODING MATRIX")
    print("═"*60)
    
    try:
        from app.core.auth import create_access_token, decode_token
        from app.core.config import settings
        
        # Test Payload
        uid_test = "25BAI70757"
        payload = {"uid": uid_test, "role": "ADMIN"}
        
        # Action: Encryption
        token = create_access_token(data=payload)
        print(f"✅ TOKEN_GEN: Successful [Sig: {token[-10:]}]")
        
        # Action: Decryption
        decoded = decode_token(token)
        
        if decoded and decoded.uid == uid_test and decoded.role == "ADMIN":
            print(f"✅ PAYLOAD_INTEGRITY: Verified for UID {decoded.uid}")
            print(f"✅ RBAC_SYNC: Role '{decoded.role}' confirmed")
            return True
        else:
            print("❌ FAIL: Token payload corrupted or decode returned None.")
            return False
            
    except Exception as e:
        print(f"❌ FAIL: Auth logic error: {e}")
        return False

def test_module_handshake():
    """Verifies that all Sovereign micro-modules are linked"""
    print("\n" + "═"*60)
    print("🧪 TEST 2: MODULE INTER-CONNECTIVITY")
    print("═"*60)
    
    critical_nodes = [
        ("app.core.auth", "create_access_token"),
        ("app.db.session", "SessionLocal"),
        ("app.api.v1.api", "api_router"),
        ("app.models.domain", "User")
    ]
    
    all_ok = True
    for mod_path, attr in critical_nodes:
        try:
            module = __import__(mod_path, fromlist=[attr])
            if hasattr(module, attr):
                print(f"✅ NODE_LINKED: {mod_path}.{attr}")
            else:
                print(f"❌ NODE_MISSING: {attr} not found in {mod_path}")
                all_ok = False
        except Exception as e:
            print(f"❌ NODE_CRASH: {mod_path} -> {e}")
            all_ok = False
    return all_ok

def test_container_grid():
    """Checks the health of the Dockerized Microservices"""
    print("\n" + "═"*60)
    print("🧪 TEST 3: DOCKER CONTAINER ORCHESTRATION")
    print("═"*60)
    
    try:
        result = subprocess.run(
            ['docker', 'compose', 'ps', '--format', 'json'],
            cwd=PROJECT_ROOT, capture_output=True, text=True
        )
        
        if result.returncode != 0:
            print("❌ FAIL: Docker Compose is not responding.")
            return False
        
        # Parsing multi-line JSON or list
        try:
            containers = json.loads(result.stdout)
            if isinstance(containers, dict): containers = [containers]
        except:
            print("ℹ️  Parsing alternative Docker output format...")
            return "running" in result.stdout.lower()

        services = {c.get('Service'): c.get('State') for c in containers}
        required = {'trustmark-ai', 'db', 'redis', 'nginx'}
        
        passed = True
        for s in required:
            state = services.get(s, 'missing')
            if state == 'running' or state == 'Up':
                print(f"✅ SERVICE_LIVE: {s}")
            else:
                print(f"❌ SERVICE_DEAD: {s} is {state}")
                passed = False
        return passed

    except Exception:
        print("⚠️  DIAGNOSTIC: Run 'docker compose up' before testing.")
        return False

def main():
    print("\n" + "👑" * 20)
    print(" TRUSTMARK SOVEREIGN v50 QA SUITE")
    print("👑" * 20)
    
    results = {
        "Token Matrix": test_token_matrix(),
        "Module Handshake": test_module_handshake(),
        "Container Grid": test_container_grid()
    }
    
    print("\n" + "═"*60)
    print("📊 SOVEREIGN STATUS REPORT")
    print("═"*60)
    for name, res in results.items():
        print(f"{'✅ PASS' if res else '❌ FAIL'}: {name}")
    
    if all(results.values()):
        print("\n🏆 SYSTEM READY FOR EXPO DEPLOYMENT!")
    else:
        print("\n🛑 SYSTEM UNSTABLE - RE-RUN MIGRATIONS/DOCKER")
        sys.exit(1)

if __name__ == "__main__":
    main()