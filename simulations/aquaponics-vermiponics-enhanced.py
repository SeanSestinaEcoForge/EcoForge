import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Enhanced Aquaponics + Vermiponics Simulation
# States:
# y[0] = F   Fish biomass (kg)
# y[1] = P   Plant biomass (kg)
# y[2] = A   Ammonia-N (mg/L)
# y[3] = I   Nitrite-N (mg/L)
# y[4] = N   Nitrate-N (mg/L)
# y[5] = S   Organic solids in media (mg/L as N equivalent)
# y[6] = DO  Dissolved oxygen (mg/L)

def aquaponics_vermiponics_model(y, t, params):
    F, P, A, I, N, S, DO = y
    
    (V, T, Q10, r_feed_base, e_feed_to_solid, e_solid_to_ammonia,
     k1_max, Km1, k2_max, Km2, r_p_max, Km_p,
     r_f_base, K_f, r_p, K_p, m_f_base,
     k_worm_base, k_reaer, k_DO_fish, k_DO_bact, k_DO_decay,
     DO_crit, DO_half) = params
    
    # Temperature correction (Q10 = 2.0–3.0 typical for biological processes)
    Q = Q10 ** ((T - 20.0) / 10.0)
    
    # Fish dynamics
    r_f = r_f_base * Q
    m_f = m_f_base * (1 + (DO_crit - DO) / DO_half if DO < DO_crit else 0)
    dF_dt = r_f * F * (1 - F / K_f) - m_f * F
    
    # Feed → solids (uneaten + feces settle → organic pool)
    feed = r_feed_base * F * Q  # temperature affects appetite/metabolism
    dS_dt = e_feed_to_solid * feed * 1000 / V   # mg/L solids-N equiv
    
    # Vermicomposting: worms break down solids → ammonia
    worm_activity = k_worm_base * Q * (DO / (DO_half + DO))  # temp + DO limited
    dS_dt -= worm_activity * S
    dA_dt = worm_activity * S * e_solid_to_ammonia
    
    # Nitrification (DO and temp limited)
    nitr1 = k1_max * Q * (DO / (DO_half + DO)) * A / (Km1 + A)
    nitr2 = k2_max * Q * (DO / (DO_half + DO)) * I / (Km2 + I)
    dA_dt -= nitr1
    dI_dt = nitr1 - nitr2
    dN_dt = nitr2
    
    # Plant uptake (nitrate preferred, temp limited)
    uptake = r_p_max * P * Q * N / (Km_p + N)
    dP_dt = r_p * (uptake / 1000) * (1 - P / K_p)  # g/day
    dN_dt -= uptake / V
    
    # Dissolved Oxygen dynamics
    reaer = k_reaer * (8.5 - DO)                    # saturation ~8.5 mg/L at 20°C
    fish_cons = k_DO_fish * F * Q / V
    bact_cons = 1.5 * (nitr1 + nitr2) / 4.57        # approx 4.57 mg O2 per mg N nitrified
    decay_cons = 0.5 * worm_activity * S / V        # rough BOD from decay
    dDO_dt = reaer - fish_cons - bact_cons - decay_cons
    
    return [dF_dt, dP_dt, dA_dt, dI_dt, dN_dt, dS_dt, dDO_dt]


# Example parameters (200 L system, ~20 °C base)
params = [
    200.0,      # V: volume (L)
    22.0,       # T: temperature (°C) — you can make this time-dependent later
    2.5,        # Q10: temperature sensitivity factor
    0.025,      # r_feed_base: feed rate (% body weight / day at 20°C)
    0.60,       # e_feed_to_solid: fraction of feed → settleable solids
    0.35,       # e_solid_to_ammonia: fraction of decayed solids → NH3-N
    3.0,        # k1_max: ammonia oxidation (mg N/L/day at 20°C)
    1.0,        # Km1
    6.0,        # k2_max: nitrite oxidation
    0.7,        # Km2
    0.8,        # r_p_max: nitrate uptake (mg N/g plant/day)
    12.0,       # Km_p
    0.015,      # r_f_base: fish growth (1/day at 20°C)
    12.0,       # K_f: carrying capacity (kg)
    0.008,      # r_p: plant growth scaling
    25.0,       # K_p: plant cap (kg)
    0.0015,     # m_f_base: base mortality (1/day)
    0.15,       # k_worm_base: worm decay rate (1/day at 20°C)
    0.8,        # k_reaer: reaeration coefficient (1/day)
    0.12,       # k_DO_fish: fish O2 consumption (mg/L per kg fish per day)
    0.0005,     # k_DO_bact: bacterial O2 use scaling
    0.0003,     # k_DO_decay: decay O2 demand
    4.0,        # DO_crit: critical DO threshold (mg/L)
    2.0         # DO_half: half-saturation for limitation
]

# Initial conditions
y0 = [1.2, 0.8, 0.1, 0.0, 8.0, 5.0, 7.5]

# Simulate 120 days
t = np.linspace(0, 120, 1200)

# Solve
solution = odeint(aquaponics_vermiponics_model, y0, t, args=(params,))

F, P, A, I, N, S, DO = solution.T

# Plotting
fig, axs = plt.subplots(4, 1, figsize=(11, 14), sharex=True)
fig.suptitle('Enhanced Aquaponics + Vermiponics Simulation (120 days)')

axs[0].plot(t, F, label='Fish biomass (kg)')
axs[0].plot(t, P, label='Plant biomass (kg)')
axs[0].legend(); axs[0].set_ylabel('Biomass')

axs[1].plot(t, A, label='Ammonia-N'); axs[1].plot(t, I, label='Nitrite-N')
axs[1].plot(t, N, label='Nitrate-N'); axs[1].plot(t, S, label='Organic solids')
axs[1].legend(); axs[1].set_ylabel('Nutrients / Solids (mg/L)')

axs[2].plot(t, DO, 'tab:cyan', label='Dissolved Oxygen (mg/L)')
axs[2].axhline(4.0, color='red', ls='--', alpha=0.6, label='Critical DO')
axs[2].legend(); axs[2].set_ylabel('DO (mg/L)')

axs[3].plot(t, N, label='Nitrate-N', color='green')
axs[3].set_ylabel('Nitrate (mg/L)'); axs[3].set_xlabel('Time (days)')
axs[3].legend()

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

# Quick stats at end
print(f"Final values (day {t[-1]:.0f}):")
print(f"  Fish: {F[-1]:.2f} kg")
print(f"  Plants: {P[-1]:.2f} kg")
print(f"  Nitrate: {N[-1]:.1f} mg/L")
print(f"  DO: {DO[-1]:.1f} mg/L")
print(f"  Organic solids: {S[-1]:.1f} mg/L")
