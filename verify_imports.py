#!/usr/bin/env python3
"""
Script to verify all imports are working correctly
"""
import sys

def test_imports():
    """Test all required imports"""
    try:
        # Test Flask imports
        import flask
        from flask import Flask, jsonify, request
        print("✓ Flask imports successful")
        
        # Test Flask extensions
        from flask_sqlalchemy import SQLAlchemy
        from flask_cors import CORS
        print("✓ Flask extensions imports successful")
        
        # Test ML libraries
        import joblib
        import numpy as np
        import sklearn
        print("✓ ML libraries imports successful")
        
        # Test our modules
        from database.db import db
        from models.db_models import RequestLog
        print("✓ Database models imports successful")
        
        # Test services
        from services.crop_service import get_crop_recommendation
        from services.fertilizer_service import get_fertilizer_recommendation
        from services.yield_service import get_yield_prediction
        from services.dosage_service import get_dosage_recommendation
        print("✓ Service functions imports successful")
        
        # Test routes
        from routes.crop_routes import crop_bp
        from routes.fertilizer_routes import fertilizer_bp
        from routes.yield_routes import yield_bp
        from routes.dosage_routes import dosage_bp
        print("✓ Route blueprints imports successful")
        
        # Test main app
        from app import app
        print("✓ Main Flask app import successful")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_app_functionality():
    """Test basic app functionality"""
    try:
        from app import app
        
        # Test app creation
        assert app is not None
        print("✓ Flask app created successfully")
        
        # Test app configuration
        assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///app.db'
        print("✓ App configuration correct")
        
        # Test blueprints registration
        blueprint_names = [bp.name for bp in app.blueprints.values()]
        expected_blueprints = ['crop', 'fertilizer', 'yield', 'dosage']
        for bp_name in expected_blueprints:
            assert bp_name in blueprint_names
        print("✓ All blueprints registered")
        
        return True
        
    except Exception as e:
        print(f"✗ App functionality error: {e}")
        return False

if __name__ == "__main__":
    print("Verifying Flask ML Backend...")
    print("=" * 40)
    
    # Test imports
    print("\nTesting imports:")
    import_success = test_imports()
    
    # Test app functionality
    print("\nTesting app functionality:")
    app_success = test_app_functionality()
    
    print("\n" + "=" * 40)
    if import_success and app_success:
        print("✅ All tests passed! The Flask backend is ready to use.")
        print("\nTo start the server, run:")
        print("python app.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

