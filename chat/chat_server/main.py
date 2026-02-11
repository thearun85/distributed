import logging
import os
from datetime import datetime, timezone

from flask import Flask, jsonify
from sqlalchemy.sql import text

from .db import get_db, init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        init_db(db_url)

    from .db import Base, engine
    from .models import User
    Base.metadata.create_all(bind=engine)

    @app.route("/health", methods=["GET"])
    def health_check():
        db_status = "disconnected"
        session = get_db()
        try:
            session.execute(text("SELECT 1"))
            session.close()
            db_status = "connected"
        except Exception as e:
            logger.error(f"DB connection failed: {e}")

        logger.info("[Distributed Chat] Fetching service status")
        return jsonify(
            {
                "app": "distributed-chat",
                "version": "0.1.0",
                "status": "healthy",
                "db_status": db_status,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        ), 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
