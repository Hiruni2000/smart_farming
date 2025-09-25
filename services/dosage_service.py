import joblib
import os
import json

# Load model once with error handling
model_path = os.path.join("models", "dosage.pkl")
try:
    dosage_model = joblib.load(model_path)
except Exception as e:
    print(f"Warning: Could not load dosage model: {e}")
    dosage_model = None

def get_dosage_recommendation(data):
    """
    Get fertilizer dosage recommendation based on soil conditions and crop requirements
    Expected input: {
        "soil_n": float,
        "soil_p": float,
        "soil_k": float,
        "ph": float,
        "crop_type": str,
        "growth_stage": str,
        "area": float
    }
    """
    try:
        if dosage_model is None:
            return {"error": "Dosage model not available. Please check model file."}
            
        # Convert categorical variables to numerical
        growth_stage_map = {"seedling": 1, "vegetative": 2, "flowering": 3, "fruiting": 4, "mature": 5}
        
        # Extract features from request
        features = [
            data["soil_n"],
            data["soil_p"],
            data["soil_k"],
            data["ph"],
            growth_stage_map.get(data["growth_stage"], 2),
            data["area"]
        ]
        
        # Get prediction
        prediction = dosage_model.predict([features])[0]
        
        return {
            "recommended_dosage": round(prediction, 2),
            "dosage_per_hectare": round(prediction / data["area"], 2),
            "application_guidelines": {
                "soil_conditions": {
                    "nitrogen": data["soil_n"],
                    "phosphorus": data["soil_p"],
                    "potassium": data["soil_k"],
                    "ph_level": data["ph"]
                },
                "crop_info": {
                    "type": data["crop_type"],
                    "growth_stage": data["growth_stage"]
                },
                "area_hectares": data["area"]
            }
        }
    except Exception as e:
        return {"error": f"Dosage recommendation failed: {str(e)}"}
