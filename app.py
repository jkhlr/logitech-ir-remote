import os
import subprocess
import time
from logging import getLogger
from pathlib import Path

import uvicorn
from fastapi import FastAPI, BackgroundTasks

logger = getLogger(__name__)
lockfile_path = Path(os.getenv('LOCKFILE_DIR', '/tmp')) / 'logitech_on.lock'
power_cmd = ['irsend', 'SEND_ONCE', 'Logitech', 'KEY_POWER']

app = FastAPI()


@app.get("/on")
async def root(delay: int = 0, background_tasks: BackgroundTasks = None):
    if not lockfile_path.exists():
        lockfile_path.touch()
        background_tasks.add_task(toggle_power, delay=delay)
    return get_status()


@app.get("/off")
async def root(delay: int = 0, background_tasks: BackgroundTasks = None):
    if lockfile_path.exists():
        lockfile_path.unlink()
        background_tasks.add_task(toggle_power, delay=delay)
    return get_status()


@app.get("/status")
async def root():
    return get_status()


def get_status():
    if lockfile_path.exists():
        return {'status': 'on'}
    return {'status': 'off'}


def toggle_power(delay=0):
    if delay:
        time.sleep(delay / 1000)
    result = subprocess.run(power_cmd, capture_output=True, text=True)
    if result.stdout:
        logger.info(result.stdout)
    if result.stderr:
        logger.warning(result.stderr)


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
