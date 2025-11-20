#Define pydantic models for REI calculations
from typing import List, Optional
from pydantic import BaseModel, Field

class REIRequest(BaseModel):

    st_coverage_kpi: float
    st_coverage_min: float
    st_coverage_max: float
    onsite_res_kpi: float
    onsite_res_min: float
    onsite_res_max: float
    net_energy_export_kpi: float
    net_energy_export_min: float
    net_energy_export_max: float
    profile: str

class REIResponse(BaseModel):
    rei_kpi_weight: float
    st_coverage_normalized: float
    onsite_res_normalized: float
    net_energy_normalized: float
    input: REIRequest