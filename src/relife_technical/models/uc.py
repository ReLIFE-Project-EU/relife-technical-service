#Define pydantic models for UC calculations
from typing import List, Optional
from pydantic import BaseModel, Field

class UCRequest(BaseModel):

    thermal_comfort_air_temp_kpi: float
    thermal_comfort_air_temp_min: float
    thermal_comfort_air_temp_max: float
    thermal_comfort_humidity_kpi: float
    thermal_comfort_humidity_min: float
    thermal_comfort_humidity_max: float
    profile: str

class UCResponse(BaseModel):
    uc_kpi_weight: float
    thermal_comfort_air_temp_normalized: float
    thermal_comfort_humidity_normalized: float
    input: UCRequest