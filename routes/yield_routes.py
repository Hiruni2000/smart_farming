from flask import Blueprint, request, jsonify
from services.yield_service import get_yield_prediction
from database.db import db
from models.db_models import RequestLog
import json

yield_bp = Blueprint("yield", __name__)

@yield_bp.route("/api/yield-prediction", methods=["POST"])
def yield_prediction():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ["area", "crop_type", "season", "rainfall", "temperature", "humidity", "soil_quality"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        result = get_yield_prediction(data)

        # Save request + result to DB
        log = RequestLog(
            module="yield",
            input_data=json.dumps(data),
            result_data=json.dumps(result)
        )
        db.session.add(log)
        db.session.commit()

        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": f"Yield prediction failed: {str(e)}"}), 500

@yield_bp.route("/api/yield-prediction", methods=["GET"])
def get_yield_logs():
    """Get recent yield prediction logs"""
    try:
        logs = RequestLog.query.filter_by(module="yield").order_by(RequestLog.id.desc()).limit(10).all()
        result = []
        for log in logs:
            result.append({
                "id": log.id,
                "input": json.loads(log.input_data),
                "result": json.loads(log.result_data),
                "timestamp": log.id  # Using ID as timestamp proxy
            })
        return jsonify({"logs": result})
    except Exception as e:
        return jsonify({"error": f"Failed to fetch logs: {str(e)}"}), 500

