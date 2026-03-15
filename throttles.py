import numpy as np

def vermi_solids_consumption(solids_kg, days, k=0.45):
    """Vermi eat solids at k=0.45/day"""
    return solids_kg * (1 - np.exp(-k * days))

def triple_throttle(pH, temp_C, alk_meq, nitrate_mgL, DO_mgL):
    """Triple pH×temp×alk matrix + nitrate feedback + DO^0.75 curve"""
    ph_factor = max(0.1, 1 - abs(pH - 7.0) / 3.0)
    temp_factor = np.exp(-((temp_C - 25) ** 2) / 50)
    alk_factor = min(1.0, alk_meq / 100.0)
    nitrate_feedback = 1 / (1 + nitrate_mgL / 15.0)
    do_factor = (DO_mgL / 8.0) ** 0.75
    return ph_factor * temp_factor * alk_factor * nitrate_feedback * do_factor

def apply_throttles(nutrient_cycle_rate, pH, temp_C, alk_meq, nitrate_mgL, DO_mgL):
    throttle = triple_throttle(pH, temp_C, alk_meq, nitrate_mgL, DO_mgL)
    return nutrient_cycle_rate * throttle
