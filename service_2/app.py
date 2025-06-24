# app.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/ping")
def ping():
    return jsonify(status="ok", service="2")

@app.route("/hello")
def hello():
    return jsonify(message="Hello from Service 2")

if __name__ == "__main__":
    # Flask app should listen on 0.0.0.0 to be accessible from other containers/host
    app.run(host="0.0.0.0", port=8002)
