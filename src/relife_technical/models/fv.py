#Define pydantic models for FV calculations
from typing import List, Optional
from pydantic import BaseModel, Field

class FVRequest(BaseModel):

    ii_kpi: float
    ii_min: float
    ii_max: float
    aoc_kpi: float
    aoc_min: float
    aoc_max: float
    irr_kpi: float
    irr_min: float
    irr_max: float
    npv_kpi: float
    npv_min: float
    npv_max: float
    profile: str

class FVResponse(BaseModel):
    fv_kpi_weight: float
    ii_normalized: float
    aoc_normalized: float
    irr_normalized: float
    npv_normalized: float
    input: FVRequest