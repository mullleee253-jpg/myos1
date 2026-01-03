#!/bin/bash
set -e

echo "=== Building MyOS ==="

# Создаём структуру
rm -rf iso
mkdir -p iso/boot/grub

# Скачиваем ядро Alpine Linux (маленькое и рабочее)
echo "=== Downloading Linux kernel ==="
wget -q --show-progress https://dl-cdn.alpinelinux.org/alpine/v3.19/releases/x86_64/netboot/vmlinuz-lts -O iso/boot/vmlinuz

# Создаём initramfs
echo "=== Building initramfs ==="
./build-initrd.sh

# Создаём GRUB конфиг
cat > iso/boot/grub/grub.cfg << 'EOF'
set timeout=3
set default=0

menuentry "MyOS" {
    linux /boot/vmlinuz quiet
    initrd /boot/initrd.img
}

menuentry "MyOS (Safe Mode)" {
    linux /boot/vmlinuz single
    initrd /boot/initrd.img
}
EOF

echo "=== Creating ISO ==="
grub-mkrescue -o myos.iso iso 2>/dev/null

echo ""
echo "=== Done! ==="
echo "ISO created: myos.iso"
ls -lh myos.iso
