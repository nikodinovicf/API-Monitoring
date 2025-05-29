from flask import jsonify
from sqlalchemy import text
import os
from app.config import db  # Import `db` directly instead of `AppConfig`
from app.metrics import Metrics

class HealthCheck:
    @staticmethod
    def check_health():
        Metrics.health_requests.inc()
        db_file_exists = os.path.exists(os.path.join(os.path.dirname(__file__), "../database/database.db"))

        try:
            db.session.execute(text("SELECT 1"))  # Direct `db` reference
            Metrics.health_status.set(1)
            return jsonify({"status": "ok", "database": "connected", "db_file": db_file_exists}), 200
        except Exception as e:
            Metrics.health_status.set(0)
            return jsonify({"status": "error", "database": "unavailable", "db_file": db_file_exists, "details": str(e)}), 500
