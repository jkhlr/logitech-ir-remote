#!/bin/bash
if [ "${ENABLE_KERNEL_MODULE}" = "1" ]; then
  modprobe lirc_dev
  modprobe lirc_rpi gpio_out_pin=24
fi
lircd --driver=default --device=/dev/lirc0

exec gunicorn app:app \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:80 \
  --log-level=info \
  --access-logfile - \
  --error-logfile -