from fastapi import APIRouter, Depends, HTTPException
from relife_technical.models.rei import REIRequest, REIResponse
from relife_technical.services.rei import calculate_rei
from relife_technical.auth.dependencies import get_authenticated_user_without_roles as get_current_user

router = APIRouter(
    prefix="/financial",
    tags=["financial"],
    responses={401: {"description": "Unauthorized"}},
)

@router.post("/rei", response_model=REIResponse, summary="Calculate REI weight")
async def rei_endpoint(
    request: REIRequest,
    #user = Depends(get_current_user),
):
    """
    Calculate the REI of Project.
    """

    try:
       rei_value = calculate_rei(
            st_coverage_kpi=request.st_coverage_kpi,
            st_coverage_min=request.st_coverage_min,
            st_coverage_max=request.st_coverage_max,
            onsite_res_kpi=request.onsite_res_kpi,
            onsite_res_min=request.onsite_res_min,
            onsite_res_max=request.onsite_res_max,
            net_energy_export_kpi=request.net_energy_export_kpi,
            net_energy_export_min=request.net_energy_export_min,
            net_energy_export_max=request.net_energy_export_max,
            profile=request.profile

        )
       return REIResponse(rei=rei_value, input=request)
    except Exception as e:
        # Return a 400 with the error message if something went wrong
        raise HTTPException(status_code=400, detail=str(e))