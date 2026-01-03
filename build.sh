#!/bin/bash
set -e

echo "=== Building MyOS ==="

# Создаём структуру
mkdir -p iso/boot/grub
mkdir -p iso/myos

# Копируем файлы системы
cp -r rootfs/* iso/myos/

# Создаём GRUB конфиг
cat > iso/boot/grub/grub.cfg << 'EOF'
set timeout=3
set default=0

menuentry "MyOS" {
    linux /boot/vmlinuz quiet splash
    initrd /boot/initrd.img
}
EOF

echo "=== Downloading minimal Linux kernel ==="
# Используем готовое ядро из Alpine Linux (очень маленькое)
if [ ! -f "iso/boot/vmlinuz" ]; then
    wget -q https://dl-cdn.alpinelinux.org/alpine/v3.19/releases/x86_64/netboot/vmlinuz-lts -O iso/boot/vmlinuz
fi

echo "=== Building initramfs with GUI ==="
./build-initrd.sh

echo "=== Creating ISO ==="
grub-mkrescue -o myos.iso iso

echo "=== Done! ==="
echo "ISO created: myos.iso"
echo "Run in VirtualBox or: qemu-system-x86_64 -cdrom myos.iso -m 512"
