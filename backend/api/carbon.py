from fastapi import APIRouter
from schemas.carbon import CarbonEstimateRequest, CarbonEstimateResponse
from services.carbon_calculator import estimate_co2

router = APIRouter()

@router.post("/calculate", response_model=CarbonEstimateResponse)
async def calculate_carbon(request: CarbonEstimateRequest):
    """
    Manually calculate CO2 savings based on waste category and weight.
    """
    result = estimate_co2(request.category, request.weight_grams)
    
    return CarbonEstimateResponse(
        success=True,
        category=result["category"],
        weight_grams=result["weight_grams"],
        co2_saved_grams=result["co2_saved_grams"],
        co2_saved_kg=result["co2_saved_kg"],
        eco_fact=result["eco_fact"]
    )
