# Phase 2: Physical Container Node Forge (Cambridge I-70/I-77 Pilot)

## ⚠️ IMPORTANT SAFETY & LIABILITY DISCLAIMER

**EcoForge designs, simulations, blueprints, code, BOMs, and all materials are provided "AS IS" and "WITH ALL FAULTS" for experimental, educational, and open-source research purposes only.**

Building or operating any EcoForge system (vermiponics, biogas digester, RO unit, solar/Powerwall integration, shipping container mods, sensors, etc.) involves **serious risks** including but not limited to:
- Fire or explosion (biogas/methane)
- Electrical shock or arc flash
- Chemical exposure or burns
- Biological hazards (pathogens, ammonia)
- Structural failure
- Flooding or system leaks
- Injury or property damage

**You assume 100% of the risk.**  
We make **no warranties** whatsoever (express or implied) about safety, performance, accuracy of simulations, or fitness for any purpose. Real-world results may differ from sims.

Always:
- Consult licensed engineers, electricians, plumbers, and local authorities
- Comply with all building, environmental, electrical, and safety codes
- Get proper permits and inspections
- Start small and test safely

**Neither Sean Sestina, EcoForge, contributors, nor any affiliates shall be liable** for any damages, injuries, losses, claims, or liabilities arising from the use of this material.

Prototype and build **at your own risk only**. Not for commercial replication without independent professional review and certification.

Read the full LICENSE (MIT) and CONTRIBUTING.md for additional terms.

**Goal**: Deploy first quick-deploy container homestead node → vermi crates + RO system running full greywater cycle, vermicast/biogas output, Grok/ESP32 monitoring live. Target: 450L/day closed-loop proof, surplus for CSA drops <10 min to Columbus.

**Dependencies**  
- Phase 1 complete (blueprint v3, BOM sourced).  
- Container secured (e.g., 20ft used shipping, insulated/floored).  
- Treasury green for final purchases if needed (fallback: bootstrap with personal/family).  

**Day-by-Day Sequence** (30–90 min daily grind + weekends push)  

**Week 1: Site & Container Prep (Days 1–7)**  
- Day 1: Secure Cambridge crossroads site access (lease/land handshake).  
- Day 2–3: Acquire/position 20ft container; level foundation (gravel/pads).  
- Day 4: Insulate walls/floor (foam + vapor barrier for temp control).  
- Day 5: Install basic solar baseline (Tesla panels + Powerwall 3 stub if available; fallback grid-tie test).  
- Day 6: Plumbing rough-in (greywater collection from mock household/kitchen).  
- Day 7: Safety baseline — electrical grounding, fire extinguisher, first aid. Checkpoint: Container habitable/secure.  

**Week 2: Vermi Reactor Build & Inoculation (Days 8–14)**  
- Day 8: Build 0.6m³ vermi bed frame (wood/IBC tote mod, 1m² x 0.6m).  
- Day 9: Layer media — bottom 10cm perlite drainage, then 55% coco coir / 35% biochar / 10% perlite (moist to 70% wet-sponge).  
- Day 10: Add 1kg garden soil + microbes; pH adjust to 6.8–7.2.  
- Day 11: Introduce 1.2–2kg Eisenia fetida (red wigglers); light kitchen scraps + 100ml 1% molasses daily.  
- Day 12–14: Acclimation ramp — increase feeds 20%/day; monitor BOD drop. Checkpoint: Bed active, worms thriving, no odors.  

**Week 3: RO System Install & Commissioning (Days 15–21)**  
- Day 15: Mount BW30 PRO-400/34 element in FRP vessel; plumb prefilter → pump → ERD → RO.  
- Day 16: Install Atlas TDS/pH/flow sensors + ESP32 board; wire to Grok node (basic logging script).  
- Day 17: Low-P flush (3bar, 30min drain); ramp to 9bar slow (<0.7bar/s).  
- Day 18: Run 1hr full drain/service; test first permeate TDS (<6ppm target).  
- Day 19–21: Integrate vermi effluent feed; ramp to 10–20% greywater blend → full by Day 21. Checkpoint: Steady flux ~18–19 LMH, permeate <6ppm, energy ~0.55 kWh/m³.  

**Week 4: Full Cycle & Grok Integration (Days 22–30)**  
- Day 22–25: Daily runs — log vermicast harvest, biogas stub test, CSA sample prep.  
- Day 26: Grok agent spawn — basic monitoring/alerts (TDS >15ppm shutdown, flow <15 LMH).  
- Day 27–28: Optimize via Grok pings (e.g., molasses dosing, pH throttle).  
- Day 29: First P2P vermicast/biogas credit test (if treasury live).  
- Day 30: Milestone — full 450L/day cycle complete, data logged, surplus output documented. Checkpoint: Node live, transparency dashboard updated with real metrics.  

**Safety & Monitoring Baselines** (ongoing)  
- Alarms: Permeate TDS >15ppm → shutdown; pH outside 6–8; flow anomalies.  
- Daily Grok logs: Temp, pH, TDS, flux, energy use.  
- Weekly review: Adjust feeds/media if fouling/BOD spikes.  

Next: Phase 3 — Optimus task chaining, multi-node scaling, full homestead hybrid. Forge nonstop till reality. 🌱⚡️🪐∞
