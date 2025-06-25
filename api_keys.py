from werkzeug.wrappers import Request, Response
from flask import Flask, request, jsonify
import configure_logging
import logging
import os 
from dotenv import load_dotenv

# Hardcoded API Key for demonstration
VALID_API_KEY = os.getenv("Key")

class Middleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        api_key = request.headers.get("X-API-KEY")

        # Validate API Key
        if not api_key or api_key != VALID_API_KEY:
            res = Response("Unauthorized: Invalid or missing API key", mimetype='text/plain', status=401)
            return res(environ, start_response)

        # Store user info in request environment
        environ["user"] = {"name": "Authorized User"}
        return self.app(environ, start_response)

app = Flask(__name__)

# Applying Middleware
app.wsgi_app = Middleware(app.wsgi_app)

@app.route("/", methods=["GET"])
def index():
    user = request.environ.get("user")
    return jsonify(message=f"Welcome, {user['name']}! Your API Key is valid.")

@app.route("/hello", methods=["GET"])
def hello():
    user = request.environ.get("user")
    return jsonify(message=f"Hello, {user['name']}! Hope you're doing great!")

@app.route("/goodbye", methods=["GET"])
def goodbye():
    user = request.environ.get("user")
    return jsonify(message=f"Goodbye, {user['name']}! Take care!")

if __name__ == "__main__":
    app.run(debug=True, port=8000)
