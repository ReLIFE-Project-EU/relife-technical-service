#ee
from typing import List

def calculate_ee(
    envelope_kpi: float,
    envelope_min: float,
    envelope_max: float,
    window_kpi: float,
    window_min: float,
    window_max: float,
    heating_system_kpi: float,
    heating_system_min: float,
    heating_system_max: float,
    cooling_system_kpi: float,
    cooling_system_min: float,
    cooling_system_max: float,
    profile: str
) -> dict:

    def normalize_low(kpi_value, min_value, max_value):
        score = (max_value - kpi_value) / (max_value - min_value) * 100
        return max(0, min(100, score))

    ee_normalized = {}

    ee_normalized["envelope"] = envelope_normalized = normalize_low(envelope_kpi, envelope_min, envelope_max)
    ee_normalized["window"] = window_normalized = normalize_low(window_kpi, window_min, window_max)
    ee_normalized["heating_system"] = heating_system_normalized = normalize_low(heating_system_kpi, heating_system_min, heating_system_max)
    ee_normalized["cooling_system"] = cooling_system_normalized = normalize_low(cooling_system_kpi, cooling_system_min, cooling_system_max)

    no_pillar = 4
    score_total = 15

    if profile == "Environment-Oriented":
        pillar_score = 3
    elif profile == "Comfort-Oriented":
        pillar_score = 2
    elif profile == "Financally-Oriented":
        pillar_score = 2
    else:
        print("Invalid profile")

    pillar_weight = pillar_score/score_total
    ee_kpi_weight = pillar_weight * (1 / no_pillar)

    return ee_kpi_weight, envelope_normalized, window_normalized, heating_system_normalized, cooling_system_normalized