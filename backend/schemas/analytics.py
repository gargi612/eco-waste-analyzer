from pydantic import BaseModel
from typing import Dict, Any

class AnalyticsResponse(BaseModel):
    success: bool
    data: Dict[str, Any]
