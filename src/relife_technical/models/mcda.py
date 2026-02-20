#Define pydantic models for MCDA calculations
from typing import Dict, List, Tuple, Optional
from pydantic import BaseModel, Field

class TechnologyKpis(BaseModel):
    name: str = Field(..., description="Technology name/identifier")

    # EE
    envelope_kpi: float
    window_kpi: float
    heating_system_kpi: float
    cooling_system_kpi: float

    # FV
    ii_kpi: float
    aoc_kpi: float
    irr_kpi: float
    npv_kpi: float
    pp_kpi: float
    arv_kpi: float

    # REI
    st_coverage_kpi: float
    onsite_res_kpi: float
    net_energy_export_kpi: float

    # SEI
    embodied_carbon_kpi: float
    gwp_kpi: float

    # UC
    thermal_comfort_air_temp_kpi: float
    thermal_comfort_humidity_kpi: float


class McdaTopsisRequest(BaseModel):
    profile: str = Field(
        ...,
        description="User profile",
        examples=["Environment-Oriented"],
    )

    technologies: List[TechnologyKpis] = Field(..., min_items=1)

    mins_maxes: Dict[str, Tuple[float, float]] = Field(
        ...,
        description=(
            "Min/max ranges"
        ),
    )


class RankedTechnology(BaseModel):
    name: str
    closeness: float
    S_plus: float
    S_minus: float


class McdaTopsisResponse(BaseModel):
    profile: str
    count: int
    ranking: List[RankedTechnology]