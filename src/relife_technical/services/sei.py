#sei
from typing import List

def calculate_sei(
    embodied_carbon_kpi: float,
    embodied_carbon_min: float,
    embodied_carbon_max: float,
    gwp_kpi: float,
    gwp_min: float,
    gwp_max: float,
    profile: str
) -> dict:

    def normalize_low(kpi_value, min_value, max_value):
        score = (max_value - kpi_value) / (max_value - min_value) * 100
        return max(0, min(100, score))

    sei_normalized = {}

    sei_normalized["embodied_carbon"] = embodied_carbon_normalized = normalize_low(embodied_carbon_kpi, embodied_carbon_min, embodied_carbon_max)
    sei_normalized["gwp"] = gwp_normalized = normalize_low(gwp_kpi, gwp_min, gwp_max)

    no_pillar = 2
    score_total = 15

    if profile == "Environment-Oriented":
        pillar_score = 1
    elif profile == "Comfort-Oriented":
        pillar_score = 4
    elif profile == "Financally-Oriented":
        pillar_score = 5
    else:
        print("Invalid profile")

    pillar_weight = pillar_score/score_total
    sei_kpi_weight = pillar_weight * (1 / no_pillar)

    return sei_kpi_weight, embodied_carbon_normalized, gwp_normalized