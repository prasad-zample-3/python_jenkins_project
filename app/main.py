from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "online",
        "message": "Welcome to the Python Microservice API"
    }), 200

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "my-python-app"
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
