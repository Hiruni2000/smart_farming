from flask import Blueprint, request, jsonify
from services.crop_service import get_crop_recommendation
from database.db import db
from models.db_models import RequestLog
import json

crop_bp = Blueprint("crop", __name__)

@crop_bp.route("/api/crop-recommendation", methods=["POST"])
def crop_recommendation():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ["soil_n", "soil_p", "soil_k", "ph", "temperature", "humidity", "rainfall"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        result = get_crop_recommendation(data)

        # Save request + result to DB
        log = RequestLog(
            module="crop",
            input_data=json.dumps(data),
            result_data=json.dumps(result)
        )
        db.session.add(log)
        db.session.commit()

        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": f"Crop recommendation failed: {str(e)}"}), 500

@crop_bp.route("/api/crop-recommendation", methods=["GET"])
def get_crop_logs():
    """Get recent crop recommendation logs"""
    try:
        logs = RequestLog.query.filter_by(module="crop").order_by(RequestLog.id.desc()).limit(10).all()
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


