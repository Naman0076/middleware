from werkzeug.wrappers import Request, Response
from flask import Flask, request, jsonify
import configure_logging
import logging
import os 
from dotenv import load_dotenv

# Hardcoded API Key for demonstration
VALID_API_KEY = os.getenv("Key")
logging.info(f"Importing Token frim env")

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
        logging.error("Unaurthorized : invalid or missing key , check the key or input")

        # Store user info in request environment
        environ["user"] = {"name": "Authorized User"}
        return self.app(environ, start_response)
logging.info*("stroing user info into the environment")

logging.info("Implementing middleware in the API")

app = Flask(__name__)

# Applying Middleware
app.wsgi_app = Middleware(app.wsgi_app)

@app.route("/", methods=["GET"])
def index():
    user = request.environ.get("user")
    return jsonify(message=f"Welcome, {user['name']}! Your API Key is valid.")
logging.info(f"Requesting basic endpoint")

@app.route("/hello", methods=["GET"])
def hello():
    user = request.environ.get("user")
    return jsonify(message=f"Hello, {user['name']}! Hope you're doing great!")
logging.info(f"Requesting /hello endpoint")

@app.route("/goodbye", methods=["GET"])
def goodbye():
    user = request.environ.get("user")
    return jsonify(message=f"Goodbye, {user['name']}! Take care!")
logging.info(f"Requesting /goodbye endpoint")

if __name__ == "__main__":
    app.run(debug=True, port=8000)
