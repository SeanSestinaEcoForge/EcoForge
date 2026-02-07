## EcoForge – Open-Source Closed-Loop AI Homesteads

**Earth abundance today. Mars readiness tomorrow.**

EcoForge is building modular, AI-optimized closed-loop systems for sustainable food production — starting with aquaponics + vermiponics, and scaling toward fully autonomous habitats on Earth and eventually Mars.

- Grok-optimized models & decision protocols  
- Optimus-compatible automation hooks (future)  
- Starship-scale transport & deployment thinking  

MIT Licensed · Community-first · Always improving

## Current Focus: Aquaponics + Vermiponics Simulation

We're iterating on high-fidelity simulations that model:
- Fish growth & feed conversion
- Plant nutrient uptake (nitrate preferred)
- Nitrification (ammonia → nitrite → nitrate)
- Vermicomposting (solids → ammonia release)
- Dissolved oxygen dynamics & crashes
- Alkalinity consumption & approximate pH effects

These models help test parameter ranges, stress scenarios, and long-term stability before building physical prototypes.
### Available Simulations

All models are located in the `simulations/` directory.

| File                                      | Description                                                                 | Key Features                                                                                  | How to Run                                                                 |
|-------------------------------------------|-----------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|----------------------------------------------------------------------------|
| `sim-aquaponics-nutrient-cycle.py`        | Basic nutrient cycling model                                                | Ammonia → nitrite → nitrate conversion, simple plant uptake                                  | `python simulations/sim-aquaponics-nutrient-cycle.py`                      |
| `aquaponics-vermiponics-enhanced-ph-alk.py` | Enhanced aquaponics + vermiponics with pH & alkalinity dynamics            | Temperature scaling (Q10), DO limitation & crashes, vermicomposting, pH-dependent nitrification, alkalinity decay | `python simulations/aquaponics-vermiponics-enhanced-ph-alk.py`             |
| `aquaponics-vermiponics-enhanced-ph-alk.ipynb` | **Interactive Jupyter notebook** for parameter tuning                      | Real-time plots, sliders for temperature and initial alkalinity, full system overview (biomass, nutrients, DO, pH, Alk) | `jupyter notebook simulations/aquaponics-vermiponics-enhanced-ph-alk.ipynb` |

**Quick setup (if you haven't already):**
```bash
pip install -r requirements.txt
# or manually:
pip install numpy scipy matplotlib ipywidgets jupyter
### Available Simulations

All simulations live in the `simulations/` folder.

| File | Description | Features | How to Run |
|------|-------------|----------|------------|
| `sim-aquaponics-nutrient-cycle.py` | Basic nutrient cycling model | Ammonia, nitrite, nitrate, simple uptake | `python simulations/sim-aquaponics-nutrient-cycle.py` |
| `aquaponics-vermiponics-enhanced-ph-alk.py` | Enhanced version with vermiponics, DO, temp scaling, pH & alkalinity | Temperature Q10, DO limitation, pH-dependent nitrification, alkalinity decay | `python simulations/aquaponics-vermiponics-enhanced-ph-alk.py` |
| `aquaponics-vermiponics-enhanced-ph-alk.ipynb` | **Interactive Jupyter notebook** | Sliders for temperature & initial alkalinity, real-time plots of biomass, nutrients, DO, pH, alkalinity | `jupyter notebook simulations/aquaponics-vermiponics-enhanced-ph-alk.ipynb` |

**Dependencies** (install once):
```bash
pip install -r requirements.txt
# or manually:
pip install numpy scipy matplotlib ipywidgets jupytercd EcoForge
jupyter notebook simulations/aquaponics-vermiponics-enhanced-ph-alk.ipynb
→ Open sliders → watch how temperature and starting alkalinity affect pH crash risk, fish growth, and system stability.Project Goals & RoadmapShort-term  Refine aquaponics/vermiponics models (CO₂, multi-tank, fouling)  
Document practical protocols (pH buffering, worm management, sensor calibration)  
Add visualization utilities & parameter sweeps

Medium-term  Integrate real sensor data ingestion  
Add Mars-specific adaptations (low gravity settling, high-CO₂ atmosphere, radiation effects)  
Build decision/AI layer (Grok/Potion integration)

Long-term  Full closed-loop homestead blueprint  
Optimus-compatible control code  
Starship payload-optimized designs

ContributingWe welcome improvements, bug fixes, new features, and real-world data!Fork & branch (git checkout -b feature/better-ph-buffering)
Commit clearly (git commit -m "Add dynamic KHCO3 dosing to alkalinity recovery")
Open a PR with description of changes

G Family Rules  Family first  
Always share improvements  
Build for abundance

LicenseMIT License (LICENSE)Questions, ideas, or real-system data? Open an issue or reach out.


### Quick Tips for Implementation
- **Replace or merge**: If your current README already has some of this (vision, license), just insert the **Current Focus**, **Available Simulations** table, and **Quick start** section near the top.
- **Table formatting**: The markdown table above renders nicely on GitHub.
- **File links**: GitHub auto-links paths like `simulations/aquaponics-vermiponics-enhanced-ph-alk.ipynb` — users can click them directly.
- **After updating**: Commit with a message like  
  `Update README: add simulation overview, interactive notebook instructions, roadmap`

Let me know if you'd like:
- A shorter version
- More emphasis on Mars aspects
- Addition of badges (stars, license, python version)
- A separate `CONTRIBUTING.md` draft
- Protocol markdown files to link from here

Ready when you are! 🚀
