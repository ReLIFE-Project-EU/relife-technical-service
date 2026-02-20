import math
from typing import Any, Dict, List, Tuple


def topsis_rank_technologies(
    technologies: List[Dict[str, Any]],
    mins_maxes: Dict[str, Tuple[float, float]],
    profile: str,
) -> List[Dict[str, Any]]:

    valid_profiles = {"Environment-Oriented", "Comfort-Oriented", "Financially-Oriented"}
    if profile not in valid_profiles:
        raise ValueError(f"Invalid profile '{profile}'. Must be one of {sorted(valid_profiles)}.")

    def mm(key: str) -> Tuple[float, float]:
        if key not in mins_maxes:
            raise KeyError(f"mins_maxes missing '{key}'")
        mn, mx = mins_maxes[key]
        if mx <= mn:
            raise ValueError(f"Invalid min/max for '{key}': max must be > min (got {mn}, {mx}).")
        return mn, mx

    def normalize_high(v: float, mn: float, mx: float) -> float:
        score = (v - mn) / (mx - mn) * 100.0
        return max(0.0, min(100.0, score))

    def normalize_low(v: float, mn: float, mx: float) -> float:
        score = (mx - v) / (mx - mn) * 100.0
        return max(0.0, min(100.0, score))

    def pillar_weight(pillar_score: int, no_kpis_in_pillar: int) -> float:
        score_total = 15
        return (pillar_score / score_total) * (1.0 / no_kpis_in_pillar)

    # Calcs
    def calculate_ee(
        envelope_kpi: float, envelope_min: float, envelope_max: float,
        window_kpi: float, window_min: float, window_max: float,
        heating_system_kpi: float, heating_system_min: float, heating_system_max: float,
        cooling_system_kpi: float, cooling_system_min: float, cooling_system_max: float,
        profile_: str
    ) -> Tuple[float, float, float, float, float]:

        envelope_n = normalize_low(envelope_kpi, envelope_min, envelope_max)
        window_n = normalize_low(window_kpi, window_min, window_max)
        heating_n = normalize_low(heating_system_kpi, heating_system_min, heating_system_max)
        cooling_n = normalize_low(cooling_system_kpi, cooling_system_min, cooling_system_max)

        if profile_ == "Environment-Oriented":
            p_score = 3
        elif profile_ == "Comfort-Oriented":
            p_score = 2
        elif profile_ == "Financially-Oriented":
            p_score = 2
        else:
            raise ValueError("Invalid profile")

        w = pillar_weight(p_score, no_kpis_in_pillar=4)
        return w, envelope_n, window_n, heating_n, cooling_n

    def calculate_fv(
        ii_kpi: float, ii_min: float, ii_max: float,
        aoc_kpi: float, aoc_min: float, aoc_max: float,
        irr_kpi: float, irr_min: float, irr_max: float,
        npv_kpi: float, npv_min: float, npv_max: float,
        pp_kpi: float, pp_min: float, pp_max: float,
        arv_kpi: float, arv_min: float, arv_max: float,
        profile_: str
    ) -> Tuple[float, float, float, float, float, float, float]:
        # FV: ii (low), aoc (low), irr (high), npv (high), pp (low), arv (high)
        ii_n = normalize_low(ii_kpi, ii_min, ii_max)
        aoc_n = normalize_low(aoc_kpi, aoc_min, aoc_max)
        irr_n = normalize_high(irr_kpi, irr_min, irr_max)
        npv_n = normalize_high(npv_kpi, npv_min, npv_max)
        pp_n = normalize_low(pp_kpi, pp_min, pp_max)
        arv_n = normalize_high(arv_kpi, arv_min, arv_max)

        if profile_ == "Environment-Oriented":
            p_score = 5
        elif profile_ == "Comfort-Oriented":
            p_score = 3
        elif profile_ == "Financially-Oriented":
            p_score = 1
        else:
            raise ValueError("Invalid profile")

        w = pillar_weight(p_score, no_kpis_in_pillar=6)
        return w, ii_n, aoc_n, irr_n, npv_n, pp_n, arv_n

    def calculate_rei(
        st_kpi: float, st_min: float, st_max: float,
        onsite_kpi: float, onsite_min: float, onsite_max: float,
        net_export_kpi: float, net_export_min: float, net_export_max: float,
        profile_: str
    ) -> Tuple[float, float, float, float]:

        st_n = normalize_high(st_kpi, st_min, st_max)
        onsite_n = normalize_high(onsite_kpi, onsite_min, onsite_max)
        net_n = normalize_high(net_export_kpi, net_export_min, net_export_max)

        if profile_ == "Environment-Oriented":
            p_score = 2
        elif profile_ == "Comfort-Oriented":
            p_score = 5
        elif profile_ == "Financially-Oriented":
            p_score = 3
        else:
            raise ValueError("Invalid profile")

        w = pillar_weight(p_score, no_kpis_in_pillar=3)
        return w, st_n, onsite_n, net_n

    def calculate_sei(
        embodied_carbon_kpi: float, embodied_carbon_min: float, embodied_carbon_max: float,
        gwp_kpi: float, gwp_min: float, gwp_max: float,
        profile_: str
    ) -> Tuple[float, float, float]:

        ec_n = normalize_low(embodied_carbon_kpi, embodied_carbon_min, embodied_carbon_max)
        gwp_n = normalize_low(gwp_kpi, gwp_min, gwp_max)

        if profile_ == "Environment-Oriented":
            p_score = 1
        elif profile_ == "Comfort-Oriented":
            p_score = 4
        elif profile_ == "Financially-Oriented":
            p_score = 5
        else:
            raise ValueError("Invalid profile")

        w = pillar_weight(p_score, no_kpis_in_pillar=2)
        return w, ec_n, gwp_n

    def calculate_uc(
        air_temp_kpi: float, air_temp_min: float, air_temp_max: float,
        humidity_kpi: float, humidity_min: float, humidity_max: float,
        profile_: str
    ) -> Tuple[float, float, float]:

        t_n = normalize_high(air_temp_kpi, air_temp_min, air_temp_max)
        rh_n = normalize_high(humidity_kpi, humidity_min, humidity_max)

        if profile_ == "Environment-Oriented":
            p_score = 4
        elif profile_ == "Comfort-Oriented":
            p_score = 1
        elif profile_ == "Financially-Oriented":
            p_score = 4
        else:
            raise ValueError("Invalid profile")

        w = pillar_weight(p_score, no_kpis_in_pillar=2)
        return w, t_n, rh_n

    required_keys = [
        "name",
        # EE
        "envelope_kpi", "window_kpi", "heating_system_kpi", "cooling_system_kpi",
        # FV
        "ii_kpi", "aoc_kpi", "irr_kpi", "npv_kpi", "pp_kpi", "arv_kpi",
        # REI
        "st_coverage_kpi", "onsite_res_kpi", "net_energy_export_kpi",
        # SEI
        "embodied_carbon_kpi", "gwp_kpi",
        # UC
        "thermal_comfort_air_temp_kpi", "thermal_comfort_humidity_kpi",
    ]

    weighted_by_tech: List[Dict[str, Any]] = []

    for tech in technologies:
        for k in required_keys:
            if k not in tech:
                raise KeyError(f"Technology '{tech.get('name', 'unknown')}' missing key '{k}'")

        # EE
        ee_w, env_n, win_n, heat_n, cool_n = calculate_ee(
            tech["envelope_kpi"], *mm("envelope_kpi"),
            tech["window_kpi"], *mm("window_kpi"),
            tech["heating_system_kpi"], *mm("heating_system_kpi"),
            tech["cooling_system_kpi"], *mm("cooling_system_kpi"),
            profile
        )

        # FV
        fv_w, ii_n, aoc_n, irr_n, npv_n, pp_n, arv_n = calculate_fv(
            tech["ii_kpi"], *mm("ii_kpi"),
            tech["aoc_kpi"], *mm("aoc_kpi"),
            tech["irr_kpi"], *mm("irr_kpi"),
            tech["npv_kpi"], *mm("npv_kpi"),
            tech["pp_kpi"], *mm("pp_kpi"),
            tech["arv_kpi"], *mm("arv_kpi"),
            profile
        )

        # REI
        rei_w, st_n, on_n, ne_n = calculate_rei(
            tech["st_coverage_kpi"], *mm("st_coverage_kpi"),
            tech["onsite_res_kpi"], *mm("onsite_res_kpi"),
            tech["net_energy_export_kpi"], *mm("net_energy_export_kpi"),
            profile
        )

        # SEI
        sei_w, ec_n, gwp_n = calculate_sei(
            tech["embodied_carbon_kpi"], *mm("embodied_carbon_kpi"),
            tech["gwp_kpi"], *mm("gwp_kpi"),
            profile
        )

        # UC
        uc_w, t_n, rh_n = calculate_uc(
            tech["thermal_comfort_air_temp_kpi"], *mm("thermal_comfort_air_temp_kpi"),
            tech["thermal_comfort_humidity_kpi"], *mm("thermal_comfort_humidity_kpi"),
            profile
        )

        weighted_kpis = {
            # EE (4)
            "envelope": ee_w * env_n,
            "window": ee_w * win_n,
            "heating_system": ee_w * heat_n,
            "cooling_system": ee_w * cool_n,

            # FV (6)
            "ii": fv_w * ii_n,
            "aoc": fv_w * aoc_n,
            "irr": fv_w * irr_n,
            "npv": fv_w * npv_n,
            "pp": fv_w * pp_n,
            "arv": fv_w * arv_n,

            # REI (3)
            "st_coverage": rei_w * st_n,
            "onsite_res": rei_w * on_n,
            "net_energy_export": rei_w * ne_n,

            # SEI (2)
            "embodied_carbon": sei_w * ec_n,
            "gwp": sei_w * gwp_n,

            # UC (2)
            "thermal_comfort_air_temp": uc_w * t_n,
            "thermal_comfort_humidity": uc_w * rh_n,
        }

        weighted_by_tech.append({"name": tech["name"], "weighted_kpis": weighted_kpis})

    if not weighted_by_tech:
        return []

    # TOPSIS ideal best/worst
    kpi_keys = list(weighted_by_tech[0]["weighted_kpis"].keys())
    ideal_best = {k: max(t["weighted_kpis"][k] for t in weighted_by_tech) for k in kpi_keys}
    ideal_worst = {k: min(t["weighted_kpis"][k] for t in weighted_by_tech) for k in kpi_keys}

    results: List[Dict[str, Any]] = []
    for t in weighted_by_tech:
        v = t["weighted_kpis"]
        s_plus = math.sqrt(sum((v[k] - ideal_best[k]) ** 2 for k in kpi_keys))
        s_minus = math.sqrt(sum((v[k] - ideal_worst[k]) ** 2 for k in kpi_keys))
        denom = s_plus + s_minus
        closeness = (s_minus / denom) if denom != 0 else 0.0

        results.append(
            {
                "name": t["name"],
                "closeness": closeness,
                "S_plus": s_plus,
                "S_minus": s_minus,
                "weighted_kpis": v,
                "ideal_best": ideal_best,
                "ideal_worst": ideal_worst,
            }
        )

    results.sort(key=lambda x: x["closeness"], reverse=True)
    return results