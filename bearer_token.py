from werkzeug.wrappers import Request, Response
from flask import Flask, request, jsonify

# Hardcoded Token for Demonstration
VALID_TOKEN = "mysecrettoken123"

class Middleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        auth_header = request.headers.get("Authorization")

        # Check if Authorization header is provided
        if not auth_header or not auth_header.startswith("Bearer "):
            res = Response("Missing or invalid token", mimetype='text/plain', status=401)
            return res(environ, start_response)

        # Extract and validate token
        token = auth_header.split(" ")[1]
        if token != VALID_TOKEN:
            res = Response("Unauthorized: Invalid token", mimetype='text/plain', status=401)
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
    return jsonify(message=f"Welcome, {user['name']}!")

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
