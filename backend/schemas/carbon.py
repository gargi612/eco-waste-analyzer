from pydantic import BaseModel

class CarbonEstimateRequest(BaseModel):
    category: str
    weight_grams: float

class CarbonEstimateResponse(BaseModel):
    success: bool
    category: str
    weight_grams: float
    co2_saved_grams: float
    co2_saved_kg: float
    eco_fact: str
