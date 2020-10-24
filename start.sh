#!/bin/bash
lircd --driver=default --device=/dev/lirc0
exec uvicorn app:app --host 0.0.0.0 --port 80