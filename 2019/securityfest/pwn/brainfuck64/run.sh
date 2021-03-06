#! /bin/bash

echo "[+] Starting challenge"

if [ "$1" == "-d" ]; then
  echo "[+] Running in Debug-mode"
	qemu-system-x86_64 \
	-m 128M \
  -s -S \
	-cpu max,+smap,+smep,check \
	-kernel ./bzImage \
	-initrd ./initramfs.cpio.gz  \
	-append 'console=ttyS0 loglevel=3 oops=panic panic=1' \
	-no-reboot \
	-nographic \
	-monitor /dev/null
else
	qemu-system-x86_64 \
	-m 128M \
	-cpu max,+smap,+smep,check \
	-kernel ./bzImage \
	-initrd ./initramfs.cpio.gz  \
	-append 'console=ttyS0 loglevel=3 oops=panic panic=1' \
	-no-reboot \
	-nographic \
	-monitor /dev/null
fi
