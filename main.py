from fastapi import FastAPI
import json
import subprocess


app = FastAPI()

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")


# Load devices from devices.json
with open("devices.json", "r") as f:
    DEVICES = json.load(f)

def ping_device(ip):
    """Ping a device and return True if reachable."""
    try:
        output = subprocess.run(
            ["ping", "-n", "1", ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return "TTL=" in output.stdout
    except:
        return False


@app.get("/devices")
def get_devices():
    return DEVICES


@app.get("/ping/{ip}")
def ping(ip: str):
    status = ping_device(ip)
    return {"ip": ip, "status": "UP" if status else "DOWN"}


@app.get("/status")
def get_status():
    results = []
    for device in DEVICES:
        alive = ping_device(device["ip"])
        results.append({
            "name": device["name"],
            "ip": device["ip"],
            "status": "UP" if alive else "DOWN"
        })
    return results
