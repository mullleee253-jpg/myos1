# Build MyOS on Windows using Docker Desktop
# Requires: Docker Desktop installed and running

Write-Host "=== Building MyOS with Docker ===" -ForegroundColor Cyan

# Check Docker
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Docker not found. Please install Docker Desktop." -ForegroundColor Red
    Write-Host "Download: https://www.docker.com/products/docker-desktop/" -ForegroundColor Yellow
    exit 1
}

# Create output directory
New-Item -ItemType Directory -Force -Path "output" | Out-Null

# Build
docker build -t myos-builder .
docker run --rm -v "${PWD}/output:/build/output" myos-builder sh -c "./build.sh && cp myos.iso output/"

Write-Host ""
Write-Host "=== Build complete! ===" -ForegroundColor Green
Write-Host "ISO file: output/myos.iso" -ForegroundColor Yellow
Write-Host ""
Write-Host "To test in VirtualBox:" -ForegroundColor Cyan
Write-Host "1. Create new VM: Type=Linux, Version=Other Linux (64-bit)"
Write-Host "2. Memory: 512 MB or more"
Write-Host "3. Settings -> Storage -> Add optical drive -> Choose output/myos.iso"
Write-Host "4. Settings -> Display -> Video Memory: 32 MB or more"
Write-Host "5. Start the VM!"
