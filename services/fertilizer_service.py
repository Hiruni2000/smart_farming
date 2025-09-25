import joblib
import os
import json

# Load model once with error handling
model_path = os.path.join("models", "fertilizer.pkl")
try:
    fertilizer_model = joblib.load(model_path)
except Exception as e:
    print(f"Warning: Could not load fertilizer model: {e}")
    fertilizer_model = None

def get_fertilizer_recommendation(data):
    """
    Get fertilizer recommendation based on soil conditions and crop type
    Expected input: {
        "soil_n": float,
        "soil_p": float, 
        "soil_k": float,
        "ph": float,
        "crop_type": str,
        "area": float
    }
    """
    try:
        if fertilizer_model is None:
            return {"error": "Fertilizer model not available. Please check model file."}
            
        # Extract features from request
        features = [
            data["soil_n"],
            data["soil_p"],
            data["soil_k"],
            data["ph"],
            data["area"]
        ]
        
        # Get prediction
        prediction = fertilizer_model.predict([features])[0]
        
        return {
            "recommended_fertilizer": prediction,
            "soil_analysis": {
                "nitrogen": data["soil_n"],
                "phosphorus": data["soil_p"],
                "potassium": data["soil_k"],
                "ph_level": data["ph"]
            },
            "area_hectares": data["area"]
        }
    except Exception as e:
        return {"error": f"Fertilizer recommendation failed: {str(e)}"}
