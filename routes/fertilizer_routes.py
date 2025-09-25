from flask import Blueprint, request, jsonify
from services.fertilizer_service import get_fertilizer_recommendation
from database.db import db
from models.db_models import RequestLog
import json

fertilizer_bp = Blueprint("fertilizer", __name__)

@fertilizer_bp.route("/api/fertilizer-recommendation", methods=["POST"])
def fertilizer_recommendation():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ["soil_n", "soil_p", "soil_k", "ph", "area"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        result = get_fertilizer_recommendation(data)

        # Save request + result to DB
        log = RequestLog(
            module="fertilizer",
            input_data=json.dumps(data),
            result_data=json.dumps(result)
        )
        db.session.add(log)
        db.session.commit()

        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": f"Fertilizer recommendation failed: {str(e)}"}), 500

@fertilizer_bp.route("/api/fertilizer-recommendation", methods=["GET"])
def get_fertilizer_logs():
    """Get recent fertilizer recommendation logs"""
    try:
        logs = RequestLog.query.filter_by(module="fertilizer").order_by(RequestLog.id.desc()).limit(10).all()
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

