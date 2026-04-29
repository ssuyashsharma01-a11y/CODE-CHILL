#!/bin/bash
# 🔐 TRUSTMARK SOVEREIGN SSL GENERATOR - v50 Platinum
# Purpose: Direct Matrix Encryption for Linux/Docker Environments

# 🎯 STEP 1: Directory Setup
mkdir -p certs
echo "📡 [MATRIX_CRYPT]: Initializing secure vault at ./certs/"

# 🎯 STEP 2: Cryptographic Handshake
# Generate 2048-bit RSA Private Key
openssl genrsa -out certs/key.pem 2048

# Generate Self-Signed Certificate with Platinum Metadata
# C=IN (India), ST=Punjab, L=Chandigarh, O=TrustMark_AI, CN=localhost
openssl req -new -x509 -key certs/key.pem -out certs/cert.pem -days 365 \
  -subj "/C=IN/ST=Punjab/L=Chandigarh/O=TrustMark_AI/OU=Biometrics_Core/CN=localhost"

# 🎯 STEP 3: Permission Shield (Crucial for Nginx/Docker)
# Set read permissions so the Nginx user can access the keys
chmod 644 certs/cert.pem
chmod 600 certs/key.pem

# 

# 🎯 STEP 4: Status Broadcast
echo ""
echo "═"x50
echo "✅ [SUCCESS]: SSL Matrix Synced for Linux!"
echo "📍 Certificate: ./certs/cert.pem"
echo "📍 Private Key: ./certs/key.pem"
echo "═"x50
echo ""
echo "⚠️  SEC_NOTICE: Self-signed certificates are for Identity Matrix testing only."
echo "🚀 NEXT STEP: Run 'docker compose up --build -d' to enable HTTPS."