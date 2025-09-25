import joblib
import os
import json

# Load model once with error handling
model_path = os.path.join("models", "crop.pkl")
try:
    crop_model = joblib.load(model_path)
except Exception as e:
    print(f"Warning: Could not load crop model: {e}")
    crop_model = None

def get_crop_recommendation(data):
    """
    Get crop recommendation based on soil and weather conditions
    Expected input: {
        "soil_n": float,
        "soil_p": float,
        "soil_k": float,
        "ph": float,
        "temperature": float,
        "humidity": float,
        "rainfall": float
    }
    """
    try:
        if crop_model is None:
            return {"error": "Crop model not available. Please check model file."}
            
        # Extract features from request
        features = [
            data["soil_n"],
            data["soil_p"],
            data["soil_k"],
            data["ph"],
            data["temperature"],
            data["humidity"],
            data["rainfall"]
        ]

        prediction = crop_model.predict([features])[0]
        return {
            "recommended_crop": prediction,
            "soil_analysis": {
                "nitrogen": data["soil_n"],
                "phosphorus": data["soil_p"],
                "potassium": data["soil_k"],
                "ph_level": data["ph"]
            },
            "weather_conditions": {
                "temperature": data["temperature"],
                "humidity": data["humidity"],
                "rainfall": data["rainfall"]
            }
        }
    except Exception as e:
        return {"error": f"Crop recommendation failed: {str(e)}"}
