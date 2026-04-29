# 🔐 TRUSTMARK SOVEREIGN SSL GENERATOR - v50 Platinum
# Purpose: Enables End-to-End Encryption for local Identity Matrix

# 🎯 STEP 1: Directory Shield
if (!(Test-Path "certs")) {
    New-Item -ItemType Directory -Path "certs" | Out-Null
}

# 🎯 STEP 2: OpenSSL Handshake Check
$opensslPath = "openssl"
try {
    & $opensslPath version | Out-Null
} catch {
    Write-Host "`n❌ [ERROR]: OpenSSL Matrix Node not found." -ForegroundColor Red
    Write-Host "💡 Solution: Install 'Git for Windows' or 'OpenSSL' to enable encryption logic."
    exit 1
}

Write-Host "`n🔄 [MATRIX_CRYPT]: Generating RSA-2048 Sovereign Certificates..." -ForegroundColor Cyan

# 🎯 STEP 3: Cryptographic Generation
# Generating 2048-bit Private Key
& $opensslPath genrsa -out certs/key.pem 2048 2>$null

# Generating Self-Signed Certificate with Platinum Metadata
# C=IN (India), ST=Punjab, L=Chandigarh (CU Region), O=TrustMark_AI, CN=localhost
& $opensslPath req -new -x509 -key certs/key.pem -out certs/cert.pem -days 365 `
  -subj "/C=IN/ST=Punjab/L=Chandigarh/O=TrustMark_AI/OU=Biometrics_Core/CN=localhost" 2>$null

# 

# 🎯 STEP 4: Verification & Deployment Instructions
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ [SUCCESS]: SSL Matrix Synced!" -ForegroundColor Green
    Write-Host "------------------------------------------------------------"
    Write-Host "📍 IDENTITY KEY: $(Resolve-Path 'certs/key.pem')"
    Write-Host "📍 PUBLIC CERT : $(Resolve-Path 'certs/cert.pem')"
    Write-Host "------------------------------------------------------------"
    
    Write-Host "`n🚀 SOVEREIGN DEPLOYMENT STEPS:" -ForegroundColor Yellow
    Write-Host "1. Move these files to your Nginx 'certs/' volume mapping."
    Write-Host "2. Ensure Nginx 'default.conf' is set to listen on Port 443 SSL."
    Write-Host "3. Run: docker compose up -d --build"
    Write-Host "4. Access securely at: https://localhost"
    Write-Host "`n⚠️  SEC_NOTICE: Browser will show 'Insecure' due to Self-Signed status."
    Write-Host "   Click 'Advanced' -> 'Proceed' to enter the Matrix."
} else {
    Write-Host "❌ [FATAL]: Cryptographic handshake failed." -ForegroundColor Red
    exit 1
}