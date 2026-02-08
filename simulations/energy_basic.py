# simulations/energy_basic.py
def daily_energy_demand(fish_tank_liters: float = 1000,
                       pumps_kw: float = 0.15,
                       lights_hours: float = 12,
                       lights_kw: float = 0.08) -> dict:
    """Rough daily kWh estimate for small homestead module"""
    pump_kwh = pumps_kw * 24
    light_kwh = lights_kw * lights_hours
    total_kwh = pump_kwh + light_kwh + 0.5  # misc (fans, sensors)

    return {
        "pump_kwh": round(pump_kwh, 2),
        "light_kwh": round(light_kwh, 2),
        "total_kwh_day": round(total_kwh, 2),
        "solar_panel_estimate": round(total_kwh_day / 4.5, 1)  # assuming 4.5 sun-hours
    }

if __name__ == "__main__":
    print(daily_energy_demand())
    # Example output: {'pump_kwh': 3.6, 'light_kwh': 0.96, 'total_kwh_day': 5.06, 'solar_panel_estimate': 1.1}
