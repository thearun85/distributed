from datetime import datetime, timezone

from flask import Flask, jsonify


def create_app():
    app = Flask(__name__)

    @app.route("/health", methods=['GET'])
    def health_check():
        return jsonify({
            "app": "distributed-chat",
            "version": "0.1.0",
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }), 200


    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
