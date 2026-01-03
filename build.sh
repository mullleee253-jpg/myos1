#!/bin/bash
set -e

echo "=== Building MyOS with GUI ==="

# Скачиваем Tiny Core Linux (минимальный Linux с X11)
echo "Downloading Tiny Core Linux base..."
mkdir -p downloads
cd downloads

if [ ! -f "vmlinuz64" ]; then
    wget -q --show-progress http://tinycorelinux.net/14.x/x86_64/release/distribution_files/vmlinuz64
fi
if [ ! -f "corepure64.gz" ]; then
    wget -q --show-progress http://tinycorelinux.net/14.x/x86_64/release/distribution_files/corepure64.gz
fi
if [ ! -f "Xlibs.tcz" ]; then
    wget -q --show-progress http://tinycorelinux.net/14.x/x86_64/tcz/Xlibs.tcz
fi
if [ ! -f "Xprogs.tcz" ]; then
    wget -q --show-progress http://tinycorelinux.net/14.x/x86_64/tcz/Xprogs.tcz
fi
if [ ! -f "Xorg-7.7.tcz" ]; then
    wget -q --show-progress http://tinycorelinux.net/14.x/x86_64/tcz/Xorg-7.7.tcz
fi
if [ ! -f "python3.11.tcz" ]; then
    wget -q --show-progress http://tinycorelinux.net/14.x/x86_64/tcz/python3.11.tcz
fi
if [ ! -f "tk-8.6.tcz" ]; then
    wget -q --show-progress http://tinycorelinux.net/14.x/x86_64/tcz/tk-8.6.tcz
fi
if [ ! -f "tcl-8.6.tcz" ]; then
    wget -q --show-progress http://tinycorelinux.net/14.x/x86_64/tcz/tcl-8.6.tcz
fi

cd ..

# Распаковываем initrd
echo "Extracting initrd..."
rm -rf initrd_root
mkdir -p initrd_root
cd initrd_root
zcat ../downloads/corepure64.gz | cpio -idm 2>/dev/null
cd ..

# Копируем наш desktop
echo "Adding MyOS desktop..."
mkdir -p initrd_root/opt/myos
cp rootfs/usr/share/myos/desktop.py initrd_root/opt/myos/

# Копируем расширения
mkdir -p initrd_root/opt/tcz
cp downloads/*.tcz initrd_root/opt/tcz/

# Создаём скрипт автозапуска
cat > initrd_root/opt/bootlocal.sh << 'EOF'
#!/bin/sh
# Load extensions
for tcz in /opt/tcz/*.tcz; do
    mount -o loop "$tcz" /mnt 2>/dev/null && cp -a /mnt/* / 2>/dev/null; umount /mnt 2>/dev/null
done

# Start X with our desktop
export DISPLAY=:0
Xorg :0 -nolisten tcp &
sleep 3
python3 /opt/myos/desktop.py &
EOF
chmod +x initrd_root/opt/bootlocal.sh

# Добавляем вызов в rc.local
echo "/opt/bootlocal.sh &" >> initrd_root/etc/init.d/tc-config

# Пакуем обратно
echo "Creating new initrd..."
cd initrd_root
find . | cpio -H newc -o 2>/dev/null | gzip > ../myos-initrd.gz
cd ..

# Создаём ISO
echo "Creating ISO..."
rm -rf iso
mkdir -p iso/boot/grub

cp downloads/vmlinuz64 iso/boot/vmlinuz
cp myos-initrd.gz iso/boot/initrd.gz

cat > iso/boot/grub/grub.cfg << 'EOF'
set timeout=3
set default=0

menuentry "MyOS" {
    linux /boot/vmlinuz quiet loglevel=3
    initrd /boot/initrd.gz
}
EOF

grub-mkrescue -o myos.iso iso 2>/dev/null

echo ""
echo "=== Build complete! ==="
ls -lh myos.iso
