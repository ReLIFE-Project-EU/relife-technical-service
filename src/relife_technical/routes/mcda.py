from fastapi import APIRouter, HTTPException, status
from relife_technical.auth.dependencies import OptionalAuthenticatedUserDep
from relife_technical.config.logging import get_logger
from relife_technical.models.mcda import (
    McdaTopsisRequest,
    McdaTopsisResponse,
    RankedTechnology,
)
from relife_technical.services.mcda_topsis import topsis_rank_technologies

router = APIRouter(tags=["mcda"], prefix="/mcda")
logger = get_logger(__name__)

@router.post("/topsis", response_model=McdaTopsisResponse)
async def run_topsis(
    payload: McdaTopsisRequest,
    current_user: OptionalAuthenticatedUserDep,
):
    try:
        technologies = [t.model_dump() for t in payload.technologies]

        logger.info(
            "Running TOPSIS ranking",
            user_id=current_user.user_id if current_user else None,
            profile=payload.profile,
            n_technologies=len(technologies),
        )

        results = topsis_rank_technologies(
            technologies=technologies,
            mins_maxes=payload.mins_maxes,
            profile=payload.profile,
        )

        ranking = [
            RankedTechnology(
                name=r["name"],
                closeness=r["closeness"],
                S_plus=r["S_plus"],
                S_minus=r["S_minus"],
            )
            for r in results
        ]

        return McdaTopsisResponse(
            profile=payload.profile,
            count=len(ranking),
            ranking=ranking,
        )

    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Missing required KPI key or mins_maxes entry: {str(e)}",
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except Exception as e:
        logger.exception("TOPSIS ranking failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to run TOPSIS ranking.",
        )
