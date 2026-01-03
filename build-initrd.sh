#!/bin/bash
set -e

echo "Building initramfs..."

INITRD_DIR="initrd_root"
rm -rf $INITRD_DIR
mkdir -p $INITRD_DIR

# Создаём структуру директорий
mkdir -p $INITRD_DIR/{bin,sbin,etc,proc,sys,dev,tmp,root,usr/bin,usr/lib,lib,lib64,run}
mkdir -p $INITRD_DIR/etc/init.d

# Скачиваем статический busybox
echo "Downloading busybox..."
wget -q --show-progress https://busybox.net/downloads/binaries/1.35.0-x86_64-linux-musl/busybox -O $INITRD_DIR/bin/busybox
chmod +x $INITRD_DIR/bin/busybox

# Создаём симлинки для busybox
cd $INITRD_DIR/bin
for cmd in sh ash bash ls cat cp mv rm mkdir rmdir mount umount sleep echo printf pwd cd clear reset stty getty login su whoami id ps kill top free df du date hostname uname dmesg mknod ln chmod chown touch head tail grep sed awk cut sort uniq wc tr vi; do
    ln -sf busybox $cmd 2>/dev/null || true
done
cd - > /dev/null

cd $INITRD_DIR/sbin
for cmd in init halt reboot poweroff switch_root; do
    ln -sf ../bin/busybox $cmd 2>/dev/null || true
done
cd - > /dev/null

# Создаём /etc/passwd и /etc/group
cat > $INITRD_DIR/etc/passwd << 'EOF'
root:x:0:0:root:/root:/bin/sh
user:x:1000:1000:User:/home/user:/bin/sh
EOF

cat > $INITRD_DIR/etc/group << 'EOF'
root:x:0:
user:x:1000:
EOF

# Создаём init скрипт
cat > $INITRD_DIR/init << 'INITEOF'
#!/bin/sh

# Mount essential filesystems
mount -t proc none /proc
mount -t sysfs none /sys
mount -t devtmpfs none /dev 2>/dev/null || mknod -m 622 /dev/console c 5 1

# Setup console
exec 0</dev/console
exec 1>/dev/console
exec 2>/dev/console

# Clear screen and show welcome
clear
echo ""
echo "  ███╗   ███╗██╗   ██╗ ██████╗ ███████╗"
echo "  ████╗ ████║╚██╗ ██╔╝██╔═══██╗██╔════╝"
echo "  ██╔████╔██║ ╚████╔╝ ██║   ██║███████╗"
echo "  ██║╚██╔╝██║  ╚██╔╝  ██║   ██║╚════██║"
echo "  ██║ ╚═╝ ██║   ██║   ╚██████╔╝███████║"
echo "  ╚═╝     ╚═╝   ╚═╝    ╚═════╝ ╚══════╝"
echo ""
echo "  Welcome to MyOS v1.0!"
echo "  Type 'help' for available commands"
echo ""
echo "============================================"
echo ""

# Set hostname
hostname myos

# Create some directories
mkdir -p /home/user
mkdir -p /var/log

# Export environment
export HOME=/root
export PATH=/bin:/sbin:/usr/bin:/usr/sbin
export TERM=linux
export PS1='myos:\w# '

# Define help function via script
cat > /bin/help << 'HELPEOF'
#!/bin/sh
echo ""
echo "MyOS Commands:"
echo "  help     - Show this help"
echo "  ls       - List files"
echo "  cd       - Change directory"
echo "  cat      - Show file contents"
echo "  clear    - Clear screen"
echo "  uname -a - System info"
echo "  free     - Memory usage"
echo "  df       - Disk usage"
echo "  ps       - Running processes"
echo "  date     - Current date/time"
echo "  reboot   - Restart system"
echo "  poweroff - Shutdown system"
echo ""
echo "Note: GUI requires X11 (not included in minimal build)"
echo ""
HELPEOF
chmod +x /bin/help

# Start shell
echo "Starting MyOS shell..."
echo ""
exec /bin/sh
INITEOF

chmod +x $INITRD_DIR/init

# Создаём initramfs
echo "Creating initrd.img..."
cd $INITRD_DIR
find . | cpio -H newc -o 2>/dev/null | gzip > ../iso/boot/initrd.img
cd ..

echo "initrd.img created successfully!"
ls -lh iso/boot/initrd.img
