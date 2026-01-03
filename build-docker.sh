#!/bin/bash
# Build MyOS using Docker (works on any OS)

echo "=== Building MyOS with Docker ==="

# Build the builder image
docker build -t myos-builder .

# Run the build
docker run --rm -v "$(pwd)/output:/build/output" myos-builder sh -c "
    ./build.sh && cp myos.iso output/
"

echo ""
echo "=== Build complete! ==="
echo "ISO file: output/myos.iso"
echo ""
echo "To test in VirtualBox:"
echo "1. Create new VM: Type=Linux, Version=Other Linux (64-bit)"
echo "2. Memory: 512 MB or more"
echo "3. Create virtual hard disk (optional)"
echo "4. Settings -> Storage -> Add optical drive -> Choose output/myos.iso"
echo "5. Settings -> Display -> Video Memory: 32 MB or more"
echo "6. Start the VM!"
