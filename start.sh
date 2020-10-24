#!/bin/bash
lircd --driver=default --device=/dev/lirc0
exec gunicorn app:app \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:80 \
  --log-level=info \
  --access-logfile - \
  --error-logfile -