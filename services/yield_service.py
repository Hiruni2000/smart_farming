import joblib
import os
import json

# Load model once with error handling
model_path = os.path.join("models", "yield.pkl")
try:
    yield_model = joblib.load(model_path)
except Exception as e:
    print(f"Warning: Could not load yield model: {e}")
    yield_model = None

def get_yield_prediction(data):
    """
    Get yield prediction based on various agricultural factors
    Expected input: {
        "area": float,
        "crop_type": str,
        "season": str,
        "rainfall": float,
        "temperature": float,
        "humidity": float,
        "soil_quality": str
    }
    """
    try:
        if yield_model is None:
            return {"error": "Yield model not available. Please check model file."}
            
        # Convert categorical variables to numerical
        season_map = {"spring": 1, "summer": 2, "autumn": 3, "winter": 4}
        soil_quality_map = {"poor": 1, "fair": 2, "good": 3, "excellent": 4}
        
        # Extract features from request
        features = [
            data["area"],
            season_map.get(data["season"], 1),
            data["rainfall"],
            data["temperature"],
            data["humidity"],
            soil_quality_map.get(data["soil_quality"], 2)
        ]
        
        # Get prediction
        prediction = yield_model.predict([features])[0]
        
        return {
            "predicted_yield": round(prediction, 2),
            "yield_per_hectare": round(prediction / data["area"], 2),
            "input_parameters": {
                "area_hectares": data["area"],
                "crop_type": data["crop_type"],
                "season": data["season"],
                "rainfall_mm": data["rainfall"],
                "temperature_celsius": data["temperature"],
                "humidity_percent": data["humidity"],
                "soil_quality": data["soil_quality"]
            }
        }
    except Exception as e:
        return {"error": f"Yield prediction failed: {str(e)}"}
