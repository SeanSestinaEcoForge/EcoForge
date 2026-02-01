# BSF Loop Accelerator – Black Soldier Fly Larvae Side-Loop
**Daily Solids → Larvae Yield → Protein/Biogas Boost**

## Purpose
Processes fish/plant solids waste into high-value protein (larvae harvest) + frass (biogas feedstock/compost). Accelerates core loop by reducing solids load, closing protein cycle.![Core Loop Flow](../images/core-loop-flow.png)

## Daily Workflow
1. Solids input: 5-15 kg/day wet waste from core loop (fish feces, plant trimmings).

2. Larvae growth: 14-21 days to prepupae.
3. Harvest: Self-harvest ramps → dry/freeze larvae (25-40% protein, high omega-3).
4. Frass output: Larvae manure → anaerobic digester for extra biogas or direct compost tea.
5. Yield calcs:
   - Conversion: 15-25% wet waste → dry larvae biomass.
   - Protein: 40-50% of dry larvae.
   - Biogas bonus: Frass VS higher than raw solids.## Core Loop Baseline Integration      Fish (Tilapia RAS) → Effluent to Plants (NFT/DWC) → Solids to BSF Loop / Digester → Biogas + Digestate → Back to System      - Tilapia density: 40-60 kg/m³      - Fouling mitigation: Air scouring + citric flush cycles      - PC drippers: 1-2 mm filtered, auto-backflush      - Biogas yield: 0.25-0.35 m³ CH₄/kg VS      

## Starter .py Snippet (bsfl_yield_calc.py – add to folder or simulations/)
```python
import numpy as np

def bsf_yield(wet_solids_kg_day, conversion_rate=0.20, dry_matter=0.30, protein_frac=0.45):
    dry_larvae = wet_solids_kg_day * conversion_rate * dry_matter
    protein_kg = dry_larvae * protein_frac
    frass_kg = wet_solids_kg_day * (1 - conversion_rate)
    return {
        'dry_larvae_kg': dry_larvae,
        'protein_kg': protein_kg,
        'frass_kg': frass_kg
    }

# Example daily
print(bsf_yield(10))  # Adjust params from trials### 3. Other Modules (e.g., biochar.md)
If separate, add `protocols/v1.1/biochar.md`:

```markdown
# Biochar Production Protocol
**Retort & Charging for Carbon Sequestration + Soil Amendment**

- Retort: Kon-Tiki or drum kiln, 400-600°C pyrolysis.
- Feedstock: Digestate solids, plant trimmings, BSF frass.
- Yield: 25-35% biochar by weight.
- Charging: Soak in compost tea + urine (nutrient loading).
- Use: Soil amendment, perchlorate sorption, pH buffer in Mars sims.
