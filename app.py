from flask import Flask, jsonify, request
import json
from flask_cors import CORS
from database.db import db
from models.db_models import RequestLog
from routes.crop_routes import crop_bp
from routes.fertilizer_routes import fertilizer_bp
from routes.yield_routes import yield_bp
from routes.dosage_routes import dosage_bp

app = Flask(__name__)
CORS(app)

# SQLite config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Register routes
app.register_blueprint(crop_bp)
app.register_blueprint(fertilizer_bp)
app.register_blueprint(yield_bp)
app.register_blueprint(dosage_bp)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/api/logs", methods=["GET"])
def get_all_logs():
    """Get all request logs with optional filtering"""
    try:
        module = request.args.get("module")  # Optional filter by module
        limit = int(request.args.get("limit", 50))  # Default limit 50
        
        query = RequestLog.query
        if module:
            query = query.filter_by(module=module)
        
        logs = query.order_by(RequestLog.timestamp.desc()).limit(limit).all()
        
        result = []
        for log in logs:
            result.append({
                "id": log.id,
                "module": log.module,
                "input": json.loads(log.input_data),
                "result": json.loads(log.result_data),
                "timestamp": log.timestamp.isoformat()
            })
        
        return jsonify({"logs": result, "count": len(result)})
    except Exception as e:
        return jsonify({"error": f"Failed to fetch logs: {str(e)}"}), 500

if __name__ == "__main__":
    with app.app_context():
        db.create_all()   # creates app.db automatically
    app.run(debug=True)
