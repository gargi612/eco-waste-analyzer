from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from schemas.prediction import PredictionResponse
from services.model_loader import classifier_service
from services.carbon_calculator import estimate_co2
from db.crud import log_prediction
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=PredictionResponse)
async def predict_waste(
    image: UploadFile = File(...),
    weight_grams: float = Form(100.0)
):
    """
    Upload an image of waste to receive AI categorization and CO2 footprint estimates.
    """
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image format (jpeg, png, etc)")
        
    try:
        image_bytes = await image.read()
    except Exception:
        raise HTTPException(status_code=400, detail="Could not read the uploaded image.")
        
    try:
        # 1. Run Inference
        prediction = classifier_service.predict(image_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference failed: {str(e)}")
        
    # 2. Estimate CO2 Footprint
    carbon_data = estimate_co2(prediction["category"], weight_grams)
    
    # 3. Log Analytics (Supabase limits execution time, consider background tasks in production)
    log_prediction(
        category=prediction["category"],
        confidence=prediction["confidence"],
        weight_grams=weight_grams,
        co2_saved_grams=carbon_data["co2_saved_grams"]
    )
    
    # 4. Return Output
    return PredictionResponse(
        success=True,
        category=prediction["category"],
        confidence=prediction["confidence"],
        weight_grams=weight_grams,
        co2_saved_grams=carbon_data["co2_saved_grams"],
        eco_fact=carbon_data["eco_fact"],
        timestamp=datetime.utcnow(),
        all_probabilities=prediction["all_probabilities"]
    )
