from flask import Flask, request
from middleware import middleware

app = Flask(__name__)

# Applying middleware
app.wsgi_app = middleware(app.wsgi_app)

@app.route("/", methods=["GET", "POST"])
def index():
    user = request.environ.get("user")
    if user:
        return f"Welcome, {user['name']}!"
    return "Unauthorized access", 401

@app.route("/hello", methods=["GET"])
def hello():
    user = request.environ.get("user")
    if user:
        return f"Hello, {user['name']}! kya haal hai !"
    return "Unauthorized access", 401

@app.route("/goodbye", methods=["GET"])
def goodbye():
    user = request.environ.get("user")
    if user:
        return f"Goodbye, {user['name']}! See you again My Bro!"
    return "Unauthorized access", 401

if __name__ == "__main__":
    app.run(debug=True, port=8000)