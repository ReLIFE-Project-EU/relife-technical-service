#Define pydantic models for EE calculations
from typing import List, Optional
from pydantic import BaseModel, Field

class EERequest(BaseModel):

    envelope_kpi: float
    envelope_min: float
    envelope_max: float
    window_kpi: float
    window_min: float
    window_max: float
    heating_system_kpi: float
    heating_system_min: float
    heating_system_max: float
    cooling_system_kpi: float
    cooling_system_min: float
    cooling_system_max: float
    profile: str

class EEResponse(BaseModel):
    ee_kpi_weight: float
    envelope_normalized: float
    window_normalized: float
    heating_system_normalized: float
    cooling_system_normalized: float
    input: EERequest