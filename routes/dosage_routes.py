from flask import Blueprint, request, jsonify
from services.dosage_service import get_dosage_recommendation
from database.db import db
from models.db_models import RequestLog
import json

dosage_bp = Blueprint("dosage", __name__)

@dosage_bp.route("/api/dosage-recommendation", methods=["POST"])
def dosage_recommendation():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ["soil_n", "soil_p", "soil_k", "ph", "crop_type", "growth_stage", "area"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        result = get_dosage_recommendation(data)

        # Save request + result to DB
        log = RequestLog(
            module="dosage",
            input_data=json.dumps(data),
            result_data=json.dumps(result)
        )
        db.session.add(log)
        db.session.commit()

        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": f"Dosage recommendation failed: {str(e)}"}), 500

@dosage_bp.route("/api/dosage-recommendation", methods=["GET"])
def get_dosage_logs():
    """Get recent dosage recommendation logs"""
    try:
        logs = RequestLog.query.filter_by(module="dosage").order_by(RequestLog.id.desc()).limit(10).all()
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

