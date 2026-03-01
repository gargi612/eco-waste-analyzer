from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class PredictionResponse(BaseModel):
    success: bool
    category: str
    confidence: float
    weight_grams: Optional[float] = None
    co2_saved_grams: Optional[float] = None
    eco_fact: Optional[str] = None
    timestamp: datetime
    all_probabilities: Dict[str, float]
    
    class Config:
        from_attributes = True
