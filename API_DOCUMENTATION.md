# Flask ML Backend API Documentation

This Flask backend provides ML-powered agricultural recommendations with SQLite database integration.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.text
```

2. Run the application:
```bash
python app.py
```

The server will start on `http://localhost:5000` with SQLite database `app.db` automatically created.

## API Endpoints

### Health Check
- **GET** `/health`
- Returns server status

### Crop Recommendation
- **POST** `/api/crop-recommendation`
- **GET** `/api/crop-recommendation` (get recent logs)

**Request Body:**
```json
{
    "soil_n": 45.0,
    "soil_p": 25.0,
    "soil_k": 30.0,
    "ph": 6.5,
    "temperature": 25.0,
    "humidity": 70.0,
    "rainfall": 150.0
}
```

**Response:**
```json
{
    "recommended_crop": "rice",
    "soil_analysis": {
        "nitrogen": 45.0,
        "phosphorus": 25.0,
        "potassium": 30.0,
        "ph_level": 6.5
    },
    "weather_conditions": {
        "temperature": 25.0,
        "humidity": 70.0,
        "rainfall": 150.0
    }
}
```

### Fertilizer Recommendation
- **POST** `/api/fertilizer-recommendation`
- **GET** `/api/fertilizer-recommendation` (get recent logs)

**Request Body:**
```json
{
    "soil_n": 45.0,
    "soil_p": 25.0,
    "soil_k": 30.0,
    "ph": 6.5,
    "area": 2.5
}
```

**Response:**
```json
{
    "recommended_fertilizer": "NPK-20-10-10",
    "soil_analysis": {
        "nitrogen": 45.0,
        "phosphorus": 25.0,
        "potassium": 30.0,
        "ph_level": 6.5
    },
    "area_hectares": 2.5
}
```

### Yield Prediction
- **POST** `/api/yield-prediction`
- **GET** `/api/yield-prediction` (get recent logs)

**Request Body:**
```json
{
    "area": 2.5,
    "crop_type": "rice",
    "season": "summer",
    "rainfall": 150.0,
    "temperature": 25.0,
    "humidity": 70.0,
    "soil_quality": "good"
}
```

**Response:**
```json
{
    "predicted_yield": 1250.5,
    "yield_per_hectare": 500.2,
    "input_parameters": {
        "area_hectares": 2.5,
        "crop_type": "rice",
        "season": "summer",
        "rainfall_mm": 150.0,
        "temperature_celsius": 25.0,
        "humidity_percent": 70.0,
        "soil_quality": "good"
    }
}
```

### Dosage Recommendation
- **POST** `/api/dosage-recommendation`
- **GET** `/api/dosage-recommendation` (get recent logs)

**Request Body:**
```json
{
    "soil_n": 45.0,
    "soil_p": 25.0,
    "soil_k": 30.0,
    "ph": 6.5,
    "crop_type": "rice",
    "growth_stage": "vegetative",
    "area": 2.5
}
```

**Response:**
```json
{
    "recommended_dosage": 125.5,
    "dosage_per_hectare": 50.2,
    "application_guidelines": {
        "soil_conditions": {
            "nitrogen": 45.0,
            "phosphorus": 25.0,
            "potassium": 30.0,
            "ph_level": 6.5
        },
        "crop_info": {
            "type": "rice",
            "growth_stage": "vegetative"
        },
        "area_hectares": 2.5
    }
}
```

### General Logs
- **GET** `/api/logs`
- Query parameters:
  - `module` (optional): Filter by module (crop, fertilizer, yield, dosage)
  - `limit` (optional): Number of logs to return (default: 50)

**Response:**
```json
{
    "logs": [
        {
            "id": 1,
            "module": "crop",
            "input": {...},
            "result": {...},
            "timestamp": "2024-01-15T10:30:00.000Z"
        }
    ],
    "count": 1
}
```

## Database Schema

### RequestLog Table
- `id`: Primary key
- `module`: Module name (crop, fertilizer, yield, dosage)
- `input_data`: JSON input data
- `result_data`: JSON output data
- `timestamp`: Request timestamp

## Error Handling

All endpoints return appropriate HTTP status codes:
- `200`: Success
- `400`: Bad Request (missing required fields)
- `500`: Internal Server Error

Error responses include a descriptive error message:
```json
{
    "error": "Missing required field: soil_n"
}
```

## ML Models

The backend uses pre-trained scikit-learn models stored as `.pkl` files:
- `models/crop.pkl`: Crop recommendation model
- `models/fertilizer.pkl`: Fertilizer recommendation model
- `models/yield.pkl`: Yield prediction model
- `models/dosage.pkl`: Dosage recommendation model

## CORS

The backend includes CORS support for cross-origin requests from web applications.

