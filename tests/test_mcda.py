import pytest
from fastapi.testclient import TestClient

from relife_technical.app import app
from relife_technical.services.mcda_topsis import (
    _PILLAR_WEIGHTS_BY_RANK,
    topsis_rank_technologies,
)

client = TestClient(app)

_ALL_KPI_KEYS = [
    "envelope_kpi",
    "window_kpi",
    "heating_system_kpi",
    "cooling_system_kpi",
    "ii_kpi",
    "aoc_kpi",
    "irr_kpi",
    "npv_kpi",
    "pp_kpi",
    "arv_kpi",
    "st_coverage_kpi",
    "onsite_res_kpi",
    "net_energy_export_kpi",
    "embodied_carbon_kpi",
    "gwp_kpi",
    "thermal_comfort_air_temp_kpi",
    "thermal_comfort_humidity_kpi",
]

_MINIMAL_TECHNOLOGY = {"name": "TechA", **{k: 50.0 for k in _ALL_KPI_KEYS}}
_MINS_MAXES = {k: [0.0, 100.0] for k in _ALL_KPI_KEYS}


def test_mcda_router_registered():
    """The mcda router must appear in the OpenAPI schema."""

    response = client.get("/openapi.json")
    assert response.status_code == 200

    paths = response.json().get("paths", {})

    assert any(
        "/mcda" in path for path in paths
    ), "No /mcda path found in OpenAPI schema — mcda router is not registered"


def test_mcda_topsis_returns_ranking():
    """A valid TOPSIS request returns a ranked list of technologies."""

    payload = {
        "profile": "Environment-Oriented",
        "technologies": [_MINIMAL_TECHNOLOGY],
        "mins_maxes": _MINS_MAXES,
    }

    response = client.post("/mcda/topsis", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["profile"] == "Environment-Oriented"
    assert data["count"] == 1
    assert len(data["ranking"]) == 1
    assert data["ranking"][0]["name"] == "TechA"
    assert "closeness" in data["ranking"][0]


def test_mcda_pillar_weights_follow_m21_methodology():
    weights = [_PILLAR_WEIGHTS_BY_RANK[rank] for rank in range(1, 6)]

    assert weights == [0.45, 0.30, 0.15, 0.08, 0.02]
    assert weights[0] > weights[-1]
    assert sum(weights) == pytest.approx(1.0)


def test_mcda_profile_can_change_the_top_ranked_technology():
    sustainability_focused = {
        **_MINIMAL_TECHNOLOGY,
        "name": "LowCarbon",
        "embodied_carbon_kpi": 0.0,
        "gwp_kpi": 0.0,
        "ii_kpi": 100.0,
        "aoc_kpi": 100.0,
        "irr_kpi": 0.0,
        "npv_kpi": 0.0,
        "pp_kpi": 100.0,
        "arv_kpi": 0.0,
    }
    financially_focused = {
        **_MINIMAL_TECHNOLOGY,
        "name": "StrongFinancials",
        "embodied_carbon_kpi": 100.0,
        "gwp_kpi": 100.0,
        "ii_kpi": 0.0,
        "aoc_kpi": 0.0,
        "irr_kpi": 100.0,
        "npv_kpi": 100.0,
        "pp_kpi": 0.0,
        "arv_kpi": 100.0,
    }
    technologies = [sustainability_focused, financially_focused]

    environmental_ranking = topsis_rank_technologies(
        technologies, _MINS_MAXES, "Environment-Oriented"
    )
    financial_ranking = topsis_rank_technologies(
        technologies, _MINS_MAXES, "Financially-Oriented"
    )

    assert environmental_ranking[0]["name"] == "LowCarbon"
    assert financial_ranking[0]["name"] == "StrongFinancials"
