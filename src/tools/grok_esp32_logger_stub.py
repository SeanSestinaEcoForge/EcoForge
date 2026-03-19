# grok_esp32_logger_stub.py
# EcoForge Grok/ESP32 sensor logging prototype
# Simulates Atlas TDS/pH/flow; logs to CSV; ready for real hardware in Phase 2

import time
import random
import csv
from datetime import datetime

LOG_FILE = "ecoforge_sensor_logs.csv"

# Blueprint v3 targets
TARGET_TDS_MAX = 6.0
TARGET_PH_MIN, TARGET_PH_MAX = 6.8, 7.2
TARGET_FLOW_MIN, TARGET_FLOW_MAX = 15.0, 20.0

def read_sensors_sim():
    tds = random.uniform(3.5, 7.5)
    ph = random.uniform(6.5, 7.5)
    flow_lmh = random.uniform(14.0, 21.0)
    energy_kwh_m3 = 0.55
    timestamp = datetime.now().isoformat()
    
    status = "nominal"
    if tds > TARGET_TDS_MAX or not (TARGET_PH_MIN <= ph <= TARGET_PH_MAX) or flow_lmh < TARGET_FLOW_MIN:
        status = "alert"
    
    return {
        "timestamp": timestamp,
        "tds_ppm": round(tds, 2),
        "ph": round(ph, 2),
        "flow_lmh": round(flow_lmh, 2),
        "energy_kwh_m3": energy_kwh_m3,
        "status": status
    }

def log_reading(data):
    print(f"[{data['timestamp']}] {data['status'].upper()}: TDS={data['tds_ppm']} ppm | pH={data['ph']} | Flow={data['flow_lmh']} LMH")
    file_exists = False
    try:
        with open(LOG_FILE, 'r') as f: file_exists = True
    except FileNotFoundError:
        pass
    with open(LOG_FILE, 'a', newline='') as csvfile:
        fieldnames = ["timestamp", "tds_ppm", "ph", "flow_lmh", "energy_kwh_m3", "status"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

if __name__ == "__main__":
    print("🌱 EcoForge Sensor Logger Stub RUNNING — simulating Grok/ESP32 metrics...")
    for i in range(15):  # 15 quick cycles
        data = read_sensors_sim()
        log_reading(data)
        time.sleep(3)  # fast for demo
    print("✅ Logs saved to ecoforge_sensor_logs.csv — ready for dashboard feed!")
