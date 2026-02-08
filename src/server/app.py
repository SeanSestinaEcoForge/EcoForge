# src/server/app.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="EcoForge Monitoring")

class ViabilityCheck(BaseModel):
    ph: float
    cell_density: float

@app.post("/viability")
async def check_viability(data: ViabilityCheck):
    status = "healthy" if 7.0 <= data.ph <= 8.5 else "critical"
    return {"status": status, "ph": data.ph, "density": data.cell_density}

# Run: uvicorn src.server.app:app --reload
