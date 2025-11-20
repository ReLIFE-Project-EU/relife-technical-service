#fv
from typing import List

def calculate_fv(
    ii_kpi: float,
    ii_min: float,
    ii_max: float,
    aoc_kpi: float,
    aoc_min: float,
    aoc_max: float,
    irr_kpi: float,
    irr_min: float,
    irr_max: float,
    npv_kpi: float,
    npv_min: float,
    npv_max: float,
    profile: str
) -> dict:

    def normalize_high(kpi_value, min_value, max_value):
        score = (kpi_value - min_value) / (max_value - min_value) * 100
        return max(0, min(100, score))

    def normalize_low(kpi_value, min_value, max_value):
        score = (max_value - kpi_value) / (max_value - min_value) * 100
        return max(0, min(100, score))

    fv_normalized = {}

    fv_normalized["ii"] = ii_normalized = normalize_low(ii_kpi, ii_min, ii_max)
    fv_normalized["aoc"] = aoc_normalized = normalize_low(aoc_kpi, aoc_min, aoc_max)
    fv_normalized["irr"] = irr_normalized = normalize_high(irr_kpi, irr_min, irr_max)
    fv_normalized["npv"] = npv_normalized = normalize_high(npv_kpi, npv_min, npv_max)

    no_pillar = 4
    score_total = 15

    if profile == "Environment-Oriented":
        pillar_score = 5
    elif profile == "Comfort-Oriented":
        pillar_score = 3
    elif profile == "Financally-Oriented":
        pillar_score = 1
    else:
        print("Invalid profile")

    pillar_weight = pillar_score/score_total
    fv_kpi_weight = pillar_weight * (1 / no_pillar)

    return fv_kpi_weight, ii_normalized, aoc_normalized, irr_normalized, npv_normalized