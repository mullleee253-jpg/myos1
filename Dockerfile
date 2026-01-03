# Dockerfile for building MyOS ISO
FROM alpine:3.19

RUN apk add --no-cache \
    grub \
    grub-bios \
    xorriso \
    mtools \
    cpio \
    gzip \
    wget \
    python3 \
    py3-tkinter \
    busybox-static

WORKDIR /build
COPY . .

RUN chmod +x build.sh build-initrd.sh

CMD ["./build.sh"]
