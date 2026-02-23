from fastapi.testclient import TestClient

from relife_technical.app import app

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
