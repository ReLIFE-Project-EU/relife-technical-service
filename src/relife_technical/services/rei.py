#rei
from typing import List

def calculate_rei(
    st_coverage_kpi: float,
    st_coverage_min: float,
    st_coverage_max: float,
    onsite_res_kpi: float,
    onsite_res_min: float,
    onsite_res_max: float,
    net_energy_export_kpi: float,
    net_energy_export_min: float,
    net_energy_export_max: float,
    profile: str
) -> dict:

    def normalize_high(kpi_value, min_value, max_value):
        score = (kpi_value - min_value) / (max_value - min_value) * 100
        return max(0, min(100, score))

    rei_normalized = {}

    rei_normalized["st_coverage"] = st_coverage_normalized = normalize_high(st_coverage_kpi, st_coverage_min, st_coverage_max)
    rei_normalized["onsite_res"] = onsite_res_normalized = normalize_high(onsite_res_kpi, onsite_res_min, onsite_res_max)
    rei_normalized["net_energy_export"] = net_energy_normalized = normalize_high(net_energy_export_kpi, net_energy_export_min, net_energy_export_max)

    no_pillar = 3
    score_total = 15

    if profile == "Environment-Oriented":
        pillar_score = 2
    elif profile == "Comfort-Oriented":
        pillar_score = 5
    elif profile == "Financally-Oriented":
        pillar_score = 3
    else:
        print("Invalid profile")

    pillar_weight = pillar_score/score_total
    rei_kpi_weight = pillar_weight * (1 / no_pillar)

    return rei_kpi_weight, st_coverage_normalized, onsite_res_normalized, net_energy_normalized