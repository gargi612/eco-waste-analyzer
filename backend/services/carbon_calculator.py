"""
Carbon Footprint Estimation Module

Responsible for calculating the estimated CO2 emissions saved based on
proper waste categorization and disposal.
Values are estimations based on standard EPA life-cycle footprint analyses.
"""

# CO2 reduction factors (grams of CO2 equivalent saved per gram of waste material properly disposed/recycled)
# Note: These are generalized averages for a gamified educational experience.
CO2_REDUCTION_FACTORS = {
    "biodegradable": 0.5,   # Composting saves methane emissions compared to landfilling
    "recyclable": 1.2,      # Average of plastic (1.5), paper (1.0), and glass (0.3)
    "hazardous": 1.8,       # E-waste and battery recycling prevents toxic pollution and virgin material mining
}

def get_co2_factor(category: str) -> float:
    """
    Returns the CO2 reduction factor for a given category.
    Defaults to 0.0 if the category is not recognized.
    """
    return CO2_REDUCTION_FACTORS.get(category.lower(), 0.0)

def estimate_co2(category: str, weight_grams: float) -> dict:
    """
    Estimates the CO2 equivalent saved based on waste category and weight.
    
    Args:
        category (str): The waste category ('biodegradable', 'recyclable', 'hazardous').
        weight_grams (float): The estimated or known weight of the waste item in grams.
        
    Returns:
        dict: A dictionary containing the category, weight, CO2 saved, and an educational fact.
    """
    category_lower = category.lower().strip()
    factor = get_co2_factor(category_lower)
    
    co2_saved_grams = factor * weight_grams
    co2_saved_kg = co2_saved_grams / 1000.0
    
    # Generate an eco-fact based on category
    eco_facts = {
        "biodegradable": "Composting organic waste reduces methane emissions from landfills, a greenhouse gas 25x more potent than CO2.",
        "recyclable": "Recycling materials like plastic and aluminum uses up to 95% less energy than producing them from raw materials.",
        "hazardous": "Properly disposing of hazardous waste prevents toxic chemicals like lead and acid from leaching into groundwater and agricultural soil."
    }
    
    fact = eco_facts.get(category_lower, "Proper waste segregation is the first step towards a circular economy.")
    
    return {
        "category": category_lower,
        "weight_grams": float(weight_grams),
        "co2_saved_grams": float(co2_saved_grams),
        "co2_saved_kg": round(co2_saved_kg, 4),
        "eco_fact": fact
    }
