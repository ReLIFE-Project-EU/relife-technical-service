from fastapi import APIRouter, Depends, HTTPException

from relife_technical.auth.dependencies import (
    get_authenticated_user_without_roles as get_current_user,
)
from relife_technical.models.sei import SEIRequest, SEIResponse
from relife_technical.services.sei import calculate_sei

router = APIRouter(
    prefix="/technical",
    tags=["technical"],
    responses={401: {"description": "Unauthorized"}},
)


@router.post("/sei", response_model=SEIResponse, summary="Calculate SEI weight")
async def sei_endpoint(
    request: SEIRequest,
    # user = Depends(get_current_user),
):
    """
    Calculate the SEI of Project.
    """

    try:
        sei_kpi_weight, embodied_carbon_normalized, gwp_normalized = calculate_sei(
            embodied_carbon_kpi=request.embodied_carbon_kpi,
            embodied_carbon_min=request.embodied_carbon_min,
            embodied_carbon_max=request.embodied_carbon_max,
            gwp_kpi=request.gwp_kpi,
            gwp_min=request.gwp_min,
            gwp_max=request.gwp_max,
            profile=request.profile,
        )

        return SEIResponse(
            sei_kpi_weight=sei_kpi_weight,
            embodied_carbon_normalized=embodied_carbon_normalized,
            gwp_normalized=gwp_normalized,
            input=request,
        )
    except Exception as e:
        # Return a 400 with the error message if something went wrong
        raise HTTPException(status_code=400, detail=str(e))
