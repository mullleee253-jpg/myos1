#!/bin/bash
set -e

echo "=== Building MyOS with GUI ==="

mkdir -p downloads iso/boot/grub

# Скачиваем Tiny Core Linux
echo "Downloading Tiny Core Linux..."
cd downloads

wget -q --show-progress -nc http://tinycorelinux.net/14.x/x86_64/release/distribution_files/vmlinuz64 || true
wget -q --show-progress -nc http://tinycorelinux.net/14.x/x86_64/release/distribution_files/rootfs64.gz || true

cd ..

# Копируем ядро
cp downloads/vmlinuz64 iso/boot/vmlinuz

# Создаём кастомный initrd с нашим desktop
echo "Creating custom initrd..."

rm -rf initrd_work
mkdir -p initrd_work
cd initrd_work

# Распаковываем оригинальный rootfs
echo "Extracting rootfs..."
zcat ../downloads/rootfs64.gz | cpio -idm 2>/dev/null || true

# Добавляем наш desktop
mkdir -p opt/myos
cp ../rootfs/usr/share/myos/desktop.py opt/myos/

# Создаём автозапуск
cat > opt/bootlocal.sh << 'BOOTEOF'
#!/bin/sh
# MyOS Startup Script

# Wait for system
sleep 2

# Check if X is available
if command -v Xorg > /dev/null 2>&1; then
    export DISPLAY=:0
    Xorg :0 -nolisten tcp vt1 &
    sleep 3
    
    if command -v python3 > /dev/null 2>&1; then
        python3 /opt/myos/desktop.py &
    elif command -v python > /dev/null 2>&1; then
        python /opt/myos/desktop.py &
    fi
fi
BOOTEOF
chmod +x opt/bootlocal.sh

# Добавляем в автозагрузку
if [ -f opt/bootsync.sh ]; then
    echo "/opt/bootlocal.sh &" >> opt/bootsync.sh
fi

# Пакуем обратно
echo "Packing initrd..."
find . | cpio -o -H newc 2>/dev/null | gzip -9 > ../iso/boot/initrd.gz

cd ..

# GRUB конфиг
cat > iso/boot/grub/grub.cfg << 'EOF'
set timeout=3
set default=0

menuentry "MyOS" {
    linux /boot/vmlinuz quiet loglevel=3 vga=791
    initrd /boot/initrd.gz
}

menuentry "MyOS (Text Mode)" {
    linux /boot/vmlinuz quiet loglevel=3
    initrd /boot/initrd.gz
}
EOF

# Создаём ISO
echo "Creating ISO..."
grub-mkrescue -o myos.iso iso 2>/dev/null

echo ""
echo "=== Build complete! ==="
ls -lh myos.iso
