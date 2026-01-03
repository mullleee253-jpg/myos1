#!/bin/bash
# Build initramfs with GUI

INITRD_DIR="initrd_root"
rm -rf $INITRD_DIR
mkdir -p $INITRD_DIR

# Create directory structure
mkdir -p $INITRD_DIR/{bin,sbin,etc,proc,sys,dev,tmp,root,usr/{bin,lib,share}}
mkdir -p $INITRD_DIR/usr/share/myos

# Copy busybox (provides basic commands)
cp /bin/busybox $INITRD_DIR/bin/ 2>/dev/null || \
    wget -q https://busybox.net/downloads/binaries/1.35.0-x86_64-linux-musl/busybox -O $INITRD_DIR/bin/busybox

chmod +x $INITRD_DIR/bin/busybox

# Create symlinks for busybox
for cmd in sh ash ls cat cp mv rm mkdir mount umount sleep echo; do
    ln -sf busybox $INITRD_DIR/bin/$cmd
done

# Copy Python and Tkinter (for GUI)
if command -v python3 &> /dev/null; then
    cp $(which python3) $INITRD_DIR/usr/bin/
    # Copy required libraries
    ldd $(which python3) | grep "=> /" | awk '{print $3}' | xargs -I {} cp {} $INITRD_DIR/usr/lib/ 2>/dev/null || true
fi

# Copy our desktop environment
cp rootfs/usr/share/myos/desktop.py $INITRD_DIR/usr/share/myos/

# Create init script
cat > $INITRD_DIR/init << 'INITEOF'
#!/bin/sh
# MyOS Init Script

# Mount essential filesystems
mount -t proc none /proc
mount -t sysfs none /sys
mount -t devtmpfs none /dev

# Set up console
exec 0</dev/console
exec 1>/dev/console
exec 2>/dev/console

echo "================================"
echo "       Welcome to MyOS          "
echo "================================"
echo ""

# Try to start X and desktop
if [ -x /usr/bin/startx ]; then
    echo "Starting graphical interface..."
    startx /usr/share/myos/desktop.py
else
    echo "Starting desktop (framebuffer mode)..."
    if [ -x /usr/bin/python3 ]; then
        export DISPLAY=:0
        python3 /usr/share/myos/desktop.py 2>/dev/null || echo "GUI failed, dropping to shell"
    fi
fi

# Fallback to shell
echo ""
echo "MyOS Shell - Type 'help' for commands"
exec /bin/sh
INITEOF

chmod +x $INITRD_DIR/init

# Create initramfs
cd $INITRD_DIR
find . | cpio -H newc -o | gzip > ../iso/boot/initrd.img
cd ..

echo "initrd.img created"
