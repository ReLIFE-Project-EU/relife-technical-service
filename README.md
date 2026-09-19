# ReLIFE Technical Service

This service ranks building renovation options using Multi-Criteria Decision Analysis (MCDA). Partners supply indicators for each option and choose a preference profile to compare energy, financial, environmental, renewable-energy, and health outcomes.

## How ranking works

`POST /mcda/topsis` applies TOPSIS, a method that scores options by their distance from ideal and least-desirable outcomes, across five pillars:

- Energy efficiency: building envelope, windows, heating, and cooling.
- Financial viability: investment, operating costs, returns, payback, and property value.
- Renewable energy integration: solar coverage, on-site generation, and energy exports.
- Environmental impact: embodied carbon and global warming potential.
- Health: avoided disability-adjusted life years (DALYs), measuring reductions in healthy life lost.

The caller supplies each option's indicators, their minimum/maximum normalization ranges, and an `Environment-Oriented`, `Health-Oriented`, or `Financially-Oriented` profile. Profiles assign different priorities to the pillars. The response contains the ordered options and their scores; higher closeness scores rank first.

Indicators must already be calculated before calling this service. See the [input/output models](src/relife_technical/models/mcda.py) and [ranking implementation](src/relife_technical/services/mcda_topsis.py).

## Run locally

Requires Python 3.11 and `uv`. From the repository root:

```bash
uv sync --frozen
uv run --frozen run-service
```

Open [API documentation](http://localhost:9090/docs); `GET /health` checks availability. `API_HOST` and `API_PORT` default to `0.0.0.0` and `9090`.

Anonymous ranking needs no authentication settings. Authenticated requests require Supabase/Keycloak credentials; see [configuration](src/relife_technical/config/settings.py). Keep credentials server-side.

Run tests with `uv run --frozen pytest`. Licensed under [EUPL-1.2](LICENSE).
