from fastapi import APIRouter, Depends, HTTPException
from relife_technical.models.ee import EERequest, EEResponse
from relife_technical.services.ee import calculate_ee
from relife_technical.auth.dependencies import get_authenticated_user_without_roles as get_current_user

router = APIRouter(
    prefix="/technical",
    tags=["technical"],
    responses={401: {"description": "Unauthorized"}},
)

@router.post("/ee", response_model=EEResponse, summary="Calculate EE weight")
async def ee_endpoint(
    request: EERequest,
    #user = Depends(get_current_user),
):
    """
    Calculate the EE of Project.
    """

    try:
       ee_value = calculate_ee(
            envelope_kpi=request.envelope_kpi,
            envelope_min=request.envelope_min,
            envelope_max=request.envelope_max,
            window_kpi=request.window_kpi,
            window_min=request.window_min,
            window_max=request.window_max,
            heating_system_kpi=request.heating_system_kpi,
            heating_system_min=request.heating_system_min,
            heating_system_max=request.heating_system_max,
            cooling_system_kpi=request.cooling_system_kpi,
            cooling_system_min=request.cooling_system_min,
            cooling_system_max=request.cooling_system_max,
            profile=request.profile

        )
       return EEResponse(ee=ee_value, input=request)
    except Exception as e:
        # Return a 400 with the error message if something went wrong
        raise HTTPException(status_code=400, detail=str(e))