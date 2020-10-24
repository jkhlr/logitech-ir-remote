import subprocess
from logging import getLogger
from pathlib import Path

import uvicorn
from fastapi import FastAPI

logger = getLogger(__name__)
lock_path = Path('/tmp/logitech_on.lock')
power_cmd = ['irsend', 'SEND_ONCE', 'Logitech', 'KEY_POWER']

app = FastAPI()


@app.get("/on")
async def root():
    if not lock_path.exists():
        lock_path.touch()
        toggle_power()
    return get_status()


@app.get("/off")
async def root():
    if lock_path.exists():
        lock_path.unlink()
        toggle_power()
    return get_status()


@app.get("/status")
async def root():
    return get_status()


def get_status():
    if lock_path.exists():
        return {'status': 'on'}
    return {'status': 'off'}


def toggle_power():
    result = subprocess.run(power_cmd, capture_output=True, text=True)
    if result.stdout:
        logger.info(result.stdout)
    if result.stderr:
        logger.warning(result.stderr)


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
