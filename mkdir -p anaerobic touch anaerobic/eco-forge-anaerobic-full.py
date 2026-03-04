# EcoForge Anaerobic Full Integrated Model
# Sean Sestina / EcoForgeProject – February 27, 2026
# Digester + Biochar/Hydrochar + 3-Stage Membrane Upgrading + Linkage
# Ready to run: python anaerobic/eco-forge-anaerobic-full.py

import numpy as np
from scipy.integrate import odeint
import pandas as pd
import matplotlib.pyplot as plt

print("EcoForge Anaerobic Module – Full Stack Loaded")
def run_full():
    print("EcoForge Anaerobic Full Run Starting...")
    
    # Fixed undefined names - placeholders (improve later)
    use_biochar = True
    use_hydrochar = False
    biochar_g_per_L = 0.0  # TODO: calculate from steady-state
    hydrochar_g_per_L = 0.0  # TODO: calculate from steady-state
    
    print(f"Additives: Biochar {use_biochar} ({biochar_g_per_L} g/L) | Hydrochar {use_hydrochar} ({hydrochar_g_per_L} g/L)")
    
    # Keep your existing sim code below...
    # Example continuation (add your t, y0, args, sol, df, etc.)
    t = np.linspace(0, 90, 901)
    y0 = [1.5, 0.8, 0.4, 800, 12, 0.0]
    args = (45.0, 50.0, 1000.0)
    
    sol = odeint(digester_ode, y0, t, args=args)
    df = pd.DataFrame(sol, columns=['S_ac', 'X_ac', 'VFA', 'TAN', 'H2S', 'CH4_rate'])
    df['time'] = t
    df['pH'] = 7.2 - 0.8 * np.log10(1 + df['VFA']/1.5 + 0.01)
    df['biogas_nm3h'] = df['CH4_rate'] * 0.35 * 0.58
    
    steady = df.iloc[-200:]
    avg_biogas = steady['biogas_nm3h'].mean()
    print(f"Average biogas: {avg_biogas:.2f} Nm³/h")    # Rest of your code...
# ────────────────────────────────────────────────
# SHARED UTILS
# ────────────────────────────────────────────────

def frac_H2S_free(pH, pKa=7.0):
    return 1 / (1 + 10**(pH - pKa))

def frac_NH3_free(pH, pKa=9.25):
    return 1 / (1 + 10**(pKa - pH))

def f_inhib_H2S(S_free, K_i=50):
    return K_i / (K_i + S_free)

def f_inhib_TAN(S_free, K_i=2500):
    return K_i / (K_i + S_free)

def yield_proxy(ORP_mV=-320, VFA=0, TAN=0):
    base = 0.35 - 0.0008 * abs(ORP_mV + 320)
    inhib = 1.0 - 0.3 * (VFA / 4.0) - 0.4 * (TAN / 3000)
    return max(0.05, base * inhib * 1.1)

def stress_factor(VFA, TAN, VFA_thresh=2.0, TAN_thresh=2000):
    return min(1.0, max(0.0, (VFA / VFA_thresh + TAN / TAN_thresh) / 2.0))

def additive_effect_factor(dose, dose_opt=10.0, k=0.8):
    effect = 1 / (1 + np.exp(-k * (dose - dose_opt)))
    if dose > 20:
        effect *= (1 - 0.02 * (dose - 20))
    return min(max(effect, 0.0), 1.0)

# ────────────────────────────────────────────────
# ADDITIVES CONFIG (Toggle here)
# ────────────────────────────────────────────────
use_biochar   = True
biochar_g_L   = 10.0
biochar_mu    = 0.40
biochar_vfa   = 0.35
biochar_relief= 0.45
biochar_yield = 0.20

use_hydrochar = True
hydrochar_g_L = 10.0
hydrochar_mu  = 0.35
hydrochar_vfa = 0.40
hydrochar_relief = 0.45
hydrochar_yield  = 0.25

bio_f  = additive_effect_factor(biochar_g_L)   if use_biochar   else 0.0
hydro_f = additive_effect_factor(hydrochar_g_L) if use_hydrochar else 0.0
add_f  = min(bio_f + hydro_f, 1.5)

# ────────────────────────────────────────────────
# DIGESTER ODE
# ────────────────────────────────────────────────

def digester_ode(y, t, S_in, Q_in, V):
    S_ac, X_ac, VFA, TAN, H2S_tot, CH4_rate = y

    pH = 7.2 - 0.8 * np.log10(1 + max(0.01, VFA / 1.5))

    H2S_free = H2S_tot * frac_H2S_free(pH)
    TAN_free = TAN * frac_NH3_free(pH)

    relief = add_f * max(biochar_relief, hydrochar_relief)
    inhib_H2S = f_inhib_H2S(H2S_free) * (1 - relief)
    inhib_TAN = f_inhib_TAN(TAN_free) * (1 - relief)

    mu_base = 0.3 * (S_ac / (0.2 + S_ac))
    mu_boost = mu_base * (1 + add_f * max(biochar_mu, hydrochar_mu))
    stress = stress_factor(VFA, TAN)
    mu_ac = mu_boost * inhib_H2S * inhib_TAN * (1 + stress * 0.25)

    r_ac = mu_ac * X_ac

    ds_ac = (Q_in/V)*(S_in - S_ac) - r_ac / 0.05
    dx_ac = (mu_ac - 0.02)*X_ac - (Q_in/V)*X_ac
    dvfa  = r_ac * 0.85 - (Q_in/V)*VFA - add_f * max(biochar_vfa, hydrochar_vfa) * VFA * (1 + stress * 0.3)
    dtan  = (Q_in/V)*(100 - TAN)  # example inlet
    dh2s  = (Q_in/V)*(5 - H2S_tot) + 0.02 * r_ac
    dch4  = r_ac * (0.35 * (1 + add_f * max(biochar_yield, hydrochar_yield)))

    return [ds_ac, dx_ac, dvfa, dtan, dh2s, dch4]

# ────────────────────────────────────────────────
# 3-STAGE MEMBRANE UPGRADING (Expanded)
# ────────────────────────────────────────────────

def stage_sep(F_in, y_CH4_in, theta, P_feed=10.0, P_perm=0.25, alpha=50.0):
    if F_in <= 0: return 0, 0, 0, 0, 0

    p_CH4_in = y_CH4_in * P_feed
    p_CO2_in = (1 - y_CH4_in) * P_feed
    p_CH4_out = p_CH4_in * (1 - theta * (1/alpha))
    p_CO2_out = p_CO2_in * (1 - theta)

    d_p_CH4 = (p_CH4_in - p_CH4_out) / np.log(p_CH4_in / p_CH4_out) if p_CH4_out > 0 else p_CH4_in
    d_p_CO2 = (p_CO2_in - p_CO2_out) / np.log(p_CO2_in / p_CO2_out) if p_CO2_out > 0 else p_CO2_in

    P_CO2 = 150.0 * 3.348e-10
    P_CH4 = P_CO2 / alpha

    J_CO2 = P_CO2 * d_p_CO2
    J_CH4 = P_CH4 * d_p_CH4

    y_CO2_p = J_CO2 / (J_CO2 + J_CH4) if (J_CO2 + J_CH4) > 0 else 0.5
    y_CH4_p = 1 - y_CO2_p

    F_perm = theta * F_in
    F_ret  = F_in - F_perm

    CH4_ret = F_in * y_CH4_in - F_perm * y_CH4_p
    y_CH4_ret = max(0.0, min(1.0, CH4_ret / F_ret if F_ret > 0 else 0))

    conv = 1 / (22.414 / 3600)
    area = (F_perm * conv) / (J_CO2 + J_CH4) if (J_CO2 + J_CH4) > 0 else 100.0

    return F_ret, y_CH4_ret, F_perm, y_CH4_p, area

def upgrade_3stage(F_feed, y_CH4_feed, theta=[0.62, 0.58, 0.52]):
    F_rec = 0.0
    y_rec = y_CH4_feed
    area_total = 0.0

    for th in theta:
        F_to = F_feed + F_rec
        y_to = (F_feed * y_CH4_feed + F_rec * y_rec) / F_to if F_to > 0 else 0

        F_r, y_r, F_p, y_p, area = stage_sep(F_to, y_to, th)
        area_total += area

        F_rec = F_r
        y_rec = y_r

    biomethane = F_r
    purity = y_r * 100
    recovery = (biomethane * y_r) / (F_feed * y_CH4_feed) * 100 if F_feed > 0 else 0
    energy = 0.30 + 0.05 * (1 - 0.25)  # vacuum example

    return {
        'biomethane_nm3h': biomethane,
        'purity_pct': purity,
        'recovery_pct': recovery,
        'area_m2': area_total,
        'energy_kwh_nm3': energy
    }

# ────────────────────────────────────────────────
# RUN FULL SIM
# ────────────────────────────────────────────────

def run_full():
    print("EcoForge Anaerobic Full Run Starting...")
    print(f"Additives: Biochar {use_biochar} ({biochar_g_per_L} g/L) | Hydrochar {use_hydrochar} ({hydrochar_g_per_L} g/L)")

    t = np.linspace(0, 90, 901)
    y0 = [1.5, 0.8, 0.4, 800, 12, 0.0]
    args = (45.0, 50.0, 1000.0)

    sol = odeint(digester_ode, y0, t, args=args)
    df = pd.DataFrame(sol, columns=['S_ac','X_ac','VFA','TAN','H2S','CH4_rate'])
    df['time'] = t
    df['pH'] = 7.2 - 0.8 * np.log10(1 + df['VFA']/1.5 + 0.01)

    df['biogas_nm3h'] = df['CH4_rate'] * 0.35 / 0.58
    df['y_CH4'] = 0.58 - 0.05 * (df['VFA']/4.0) + 0.02 * np.random.normal(0,0.02,len(df))

    steady = df.iloc[-200:]
    avg_biogas = steady['biogas_nm3h'].mean()
    avg_y = steady['y_CH4'].mean()

    print(f"\nSteady biogas feed: {avg_biogas:.1f} Nm³/h @ {avg_y*100:.1f}% CH₄")

    up = upgrade_3stage(avg_biogas, avg_y)

    print("\nUpgrading Results:")
    for k, v in up.items():
        print(f"  {k}: {v:.2f}")

    # Plot
    fig, ax1 = plt.subplots(figsize=(12,6))
    ax1.plot(df['time'], df['biogas_nm3h'], 'teal', label='Biogas (Nm³/h)')
    ax1.set_ylabel('Biogas Flow')
    ax1.legend(loc='upper left')

    ax2 = ax1.twinx()
    ax2.plot(df['time'], df['VFA'], 'orange', label='VFA')
    ax2.plot(df['time'], df['TAN']/1000, 'purple', label='TAN (g/L)')
    ax2.set_ylabel('VFA / TAN')
    ax2.legend(loc='upper right')

    plt.title("EcoForge Anaerobic Full Run")
    plt.xlabel("Time (days)")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

    return df, up


if __name__ == "__main__":
    digester_df, upgrading_results = run_full()
