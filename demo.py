from werkzeug.wrappers import Request, Response
from flask import Flask, request
from basic_auth_middleware import basicauthmiddleware

app = Flask(__name__)

# Applying Middleware
app.wsgi_app = basicauthmiddleware(app.wsgi_app)

@app.route("/", methods=["GET"])
def index():
    user = request.environ.get("user")
    if user:
        return f"Welcome, {user['name']}!"
    return "Unauthorized access", 401

@app.route("/hello", methods=["GET"])
def hello():
    user = request.environ.get("user")
    if user:
        return f"Hello, {user['name']}! Hope you're doing great!"
    return "Unauthorized access", 401

@app.route("/goodbye", methods=["GET"])
def goodbye():
    user = request.environ.get("user")
    if user:
        return f"Goodbye, {user['name']}! Take care!"
    return "Unauthorized access", 401

if __name__ == "__main__":
    app.run(debug=True, port=8000)
