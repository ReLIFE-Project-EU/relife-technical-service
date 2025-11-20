#uc
from typing import List

def calculate_uc(
    thermal_comfort_air_temp_kpi: float,
    thermal_comfort_air_temp_min: float,
    thermal_comfort_air_temp_max: float,
    thermal_comfort_humidity_kpi: float,
    thermal_comfort_humidity_min: float,
    thermal_comfort_humidity_max: float,
    profile: str
) -> dict:

    def normalize_high(kpi_value, min_value, max_value):
        score = (kpi_value - min_value) / (max_value - min_value) * 100
        return max(0, min(100, score))

    uc_normalized = {}

    uc_normalized["thermal_comfort_air_temp"] = thermal_comfort_air_temp_normalized = normalize_high(thermal_comfort_air_temp_kpi, thermal_comfort_air_temp_min, thermal_comfort_air_temp_max)
    uc_normalized["thermal_comfort_humidity"] = thermal_comfort_humidity_normalized = normalize_high(thermal_comfort_humidity_kpi, thermal_comfort_humidity_min, thermal_comfort_humidity_max)
    
    no_pillar = 2
    score_total = 15

    if profile == "Environment-Oriented":
        pillar_score = 4
    elif profile == "Comfort-Oriented":
        pillar_score = 1
    elif profile == "Financally-Oriented":
        pillar_score = 4
    else:
        print("Invalid profile")

    pillar_weight = pillar_score/score_total
    uc_kpi_weight = pillar_weight * (1 / no_pillar)

    return uc_kpi_weight, thermal_comfort_air_temp_normalized, thermal_comfort_humidity_normalized