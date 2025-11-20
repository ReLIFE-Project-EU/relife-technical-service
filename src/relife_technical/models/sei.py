#Define pydantic models for SEI calculations
from typing import List, Optional
from pydantic import BaseModel, Field

class SEIRequest(BaseModel):

    embodied_carbon_kpi: float
    embodied_carbon_min: float
    embodied_carbon_max: float
    gwp_kpi: float
    gwp_min: float
    gwp_max: float
    profile: str

class SEIResponse(BaseModel):
    sei_kpi_weight: float
    embodied_carbon_normalized: float
    gwp_normalized: float
    input: SEIRequest