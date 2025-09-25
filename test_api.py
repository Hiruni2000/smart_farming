#!/usr/bin/env python3
"""
Simple test script for the Flask ML Backend API
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_crop_recommendation():
    """Test crop recommendation endpoint"""
    try:
        data = {
            "soil_n": 45.0,
            "soil_p": 25.0,
            "soil_k": 30.0,
            "ph": 6.5,
            "temperature": 25.0,
            "humidity": 70.0,
            "rainfall": 150.0
        }
        response = requests.post(f"{BASE_URL}/api/crop-recommendation", json=data)
        print(f"Crop recommendation: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Crop recommendation test failed: {e}")
        return False

def test_fertilizer_recommendation():
    """Test fertilizer recommendation endpoint"""
    try:
        data = {
            "soil_n": 45.0,
            "soil_p": 25.0,
            "soil_k": 30.0,
            "ph": 6.5,
            "area": 2.5
        }
        response = requests.post(f"{BASE_URL}/api/fertilizer-recommendation", json=data)
        print(f"Fertilizer recommendation: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Fertilizer recommendation test failed: {e}")
        return False

def test_yield_prediction():
    """Test yield prediction endpoint"""
    try:
        data = {
            "area": 2.5,
            "crop_type": "rice",
            "season": "summer",
            "rainfall": 150.0,
            "temperature": 25.0,
            "humidity": 70.0,
            "soil_quality": "good"
        }
        response = requests.post(f"{BASE_URL}/api/yield-prediction", json=data)
        print(f"Yield prediction: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Yield prediction test failed: {e}")
        return False

def test_dosage_recommendation():
    """Test dosage recommendation endpoint"""
    try:
        data = {
            "soil_n": 45.0,
            "soil_p": 25.0,
            "soil_k": 30.0,
            "ph": 6.5,
            "crop_type": "rice",
            "growth_stage": "vegetative",
            "area": 2.5
        }
        response = requests.post(f"{BASE_URL}/api/dosage-recommendation", json=data)
        print(f"Dosage recommendation: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Dosage recommendation test failed: {e}")
        return False

def test_logs():
    """Test logs endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/logs")
        print(f"Logs: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Logs test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Flask ML Backend API...")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health),
        ("Crop Recommendation", test_crop_recommendation),
        ("Fertilizer Recommendation", test_fertilizer_recommendation),
        ("Yield Prediction", test_yield_prediction),
        ("Dosage Recommendation", test_dosage_recommendation),
        ("Logs", test_logs)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 30)
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("Test Results Summary:")
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nOverall: {passed}/{total} tests passed")

