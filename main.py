from fastapi import FastAPI
import json
import subprocess
from datetime import datetime
import random


app = FastAPI()

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")



@app.get("/api/latency")
def get_latency():
    return {
        "timestamps": [
            datetime.now().strftime("%H:%M:%S")
            for _ in range(5)
        ],
        "latencies": [random.randint(10, 100) for _ in range(5)]
    }



# Load devices from devices.json
with open("devices.json", "r") as f:
    DEVICES = json.load(f)

def ping_device(ip):
    """
    Returns:
    - status: UP / DOWN
    - latency: response time in ms or None
    """
    try:
        output = subprocess.run(
            ["ping", "-n", "1", ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if "TTL=" in output.stdout:
            # Extract time=XXms
            for line in output.stdout.split("\n"):
                if "time=" in line:
                    latency = line.split("time=")[1].split("ms")[0]
                    return "UP", int(latency)
            return "UP", None

        return "DOWN", None
    except:
        return "DOWN", None



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
        status, latency = ping_device(device["ip"])
        results.append({
            "name": device["name"],
            "ip": device["ip"],
            "status": status,
            "latency": latency
        })
    return results

