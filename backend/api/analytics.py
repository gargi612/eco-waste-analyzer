from fastapi import APIRouter
from schemas.analytics import AnalyticsResponse
from db.crud import get_analytics

router = APIRouter()

@router.get("/dashboard", response_model=AnalyticsResponse)
async def get_dashboard_analytics():
    """
    Retrieve global or user-specific aggregated analytics from Supabase.
    """
    data = get_analytics()
    return AnalyticsResponse(
        success=True,
        data=data
    )
