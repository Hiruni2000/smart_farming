from database.db import db
from datetime import datetime

class RequestLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module = db.Column(db.String(50))  # crop / fertilizer / yield / dosage
    input_data = db.Column(db.Text)    # JSON input
    result_data = db.Column(db.Text)   # JSON output
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
