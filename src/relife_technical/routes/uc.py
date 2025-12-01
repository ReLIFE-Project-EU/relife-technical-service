from fastapi import APIRouter, Depends, HTTPException

from relife_technical.auth.dependencies import (
    get_authenticated_user_without_roles as get_current_user,
)
from relife_technical.models.uc import UCRequest, UCResponse
from relife_technical.services.uc import calculate_uc

router = APIRouter(
    prefix="/technical",
    tags=["technical"],
    responses={401: {"description": "Unauthorized"}},
)


@router.post("/uc", response_model=UCResponse, summary="Calculate UC weight")
async def uc_endpoint(
    request: UCRequest,
    # user = Depends(get_current_user),
):
    """
    Calculate the UC of Project.
    """

    try:
        (
            uc_kpi_weight,
            thermal_comfort_air_temp_normalized,
            thermal_comfort_humidity_normalized,
        ) = calculate_uc(
            thermal_comfort_air_temp_kpi=request.thermal_comfort_air_temp_kpi,
            thermal_comfort_air_temp_min=request.thermal_comfort_air_temp_min,
            thermal_comfort_air_temp_max=request.thermal_comfort_air_temp_max,
            thermal_comfort_humidity_kpi=request.thermal_comfort_humidity_kpi,
            thermal_comfort_humidity_min=request.thermal_comfort_humidity_min,
            thermal_comfort_humidity_max=request.thermal_comfort_humidity_max,
            profile=request.profile,
        )

        return UCResponse(
            uc_kpi_weight=uc_kpi_weight,
            thermal_comfort_air_temp_normalized=thermal_comfort_air_temp_normalized,
            thermal_comfort_humidity_normalized=thermal_comfort_humidity_normalized,
            input=request,
        )
    except Exception as e:
        # Return a 400 with the error message if something went wrong
        raise HTTPException(status_code=400, detail=str(e))
