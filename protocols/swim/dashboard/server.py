from flask import Flask, send_from_directory
from flask_cors import CORS
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
CORS(app)

@app.route("/dashboard", methods=['GET'])
def dashboard():
    return send_from_directory(BASE_DIR, "index.html")

@app.route("/<path:filename>", methods=['GET'])
def get_static(filename):
    return send_from_directory(BASE_DIR, filename)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
