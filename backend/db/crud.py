from db.supabase_client import supabase_client
from datetime import datetime

# Temporary in-memory cache for analytics if Supabase is offline
_mock_records = []

def log_prediction(category: str, confidence: float, weight_grams: float, co2_saved_grams: float):
    data = {
        "category": category,
        "confidence": confidence,
        "weight_grams": weight_grams,
        "co2_saved_grams": co2_saved_grams,
        "created_at": datetime.utcnow().isoformat()
    }
    
    if not supabase_client:
        _mock_records.append(data)
        return data
        
    try:
        response = supabase_client.table("predictions").insert(data).execute()
        return response.data
    except Exception as e:
        print(f"[ERROR] Failed to log to Supabase: {e}")
        _mock_records.append(data)
        return None

def get_analytics():
    if not supabase_client:
        records = _mock_records
    else:
        try:
            response = supabase_client.table("predictions").select("*").execute()
            records = response.data
        except Exception as e:
            print(f"[ERROR] Failed to fetch analytics: {e}")
            records = _mock_records
        
    total_co2 = sum(r.get("co2_saved_grams", 0) for r in records) / 1000.0 # Standardize to kg
    breakdown = {}
    
    for r in records:
        cat = r.get("category", "unknown")
        breakdown[cat] = breakdown.get(cat, 0) + 1
        
    return {
        "total_scans": len(records),
        "total_co2_saved_kg": round(total_co2, 2),
        "breakdown": breakdown
    }
