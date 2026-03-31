# Add this function somewhere
def co2_dynamics(plant_biomass_g: float,
                 fish_respiration_rate: float = 0.002,  # g CO2 / g fish / h
                 fish_biomass_g: float = 5000,
                 hours: float = 24) -> float:
    plant_consumption = 0.0015 * plant_biomass_g * hours  # rough photosynthesis
    fish_production = fish_respiration_rate * fish_biomass_g * hours
    net_co2_g = fish_production - plant_consumption
    return net_co2_g / 1000  # kg/day# src/sensors/sensor_loader_stub.py
import pandas as pd

def load_sensor_csv(path: str) -> pd.DataFrame:
    """Stub for future real sensor ingestion"""
    try:
        df = pd.read_csv(path, parse_dates=['timestamp'])
        df = df[['timestamp', 'ph', 'do_mg_l', 'temp_c', 'ammonia_mg_l']]
        return df
    except Exception as e:
        print(f"Error loading sensor data: {e}")
        return pd.DataFrame()

# Later: connect to MQTT, InfluxDB, etc.# src/utils/state_logger.py
import json
from datetime import datetime

def save_sim_state(state: dict, filename: str = "sim_state_latest.json"):
    state["timestamp"] = datetime.utcnow().isoformat()
    with open(filename, "w") as f:
        json.dump(state, f, indent=2)
    print(f"State saved to {filename}")
