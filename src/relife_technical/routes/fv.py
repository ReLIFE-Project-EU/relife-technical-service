from fastapi import APIRouter, Depends, HTTPException
from relife_technical.models.fv import FVRequest, FVResponse
from relife_technical.services.fv import calculate_fv
from relife_technical.auth.dependencies import get_authenticated_user_without_roles as get_current_user

router = APIRouter(
    prefix="/technical",
    tags=["technical"],
    responses={401: {"description": "Unauthorized"}},
)

@router.post("/fv", response_model=FVResponse, summary="Calculate FV weight")
async def fv_endpoint(
    request: FVRequest,
    #user = Depends(get_current_user),
):
    """
    Calculate the FV of Project.
    """

    try:
       fv_value = calculate_fv(
            ii_kpi=request.ii_kpi,
            ii_min=request.ii_min,
            ii_max=request.ii_max,
            aoc_kpi=request.aoc_kpi,
            aoc_min=request.aoc_min,
            aoc_max=request.aoc_max,
            irr_kpi=request.irr_kpi,
            irr_min=request.irr_min,
            irr_max=request.irr_max,
            npv_kpi=request.npv_kpi,
            npv_min=request.npv_min,
            npv_max=request.npv_max,
            profile=request.profile

        )
       return FVResponse(fv=fv_value, input=request)
    except Exception as e:
        # Return a 400 with the error message if something went wrong
        raise HTTPException(status_code=400, detail=str(e))