import jwt
import datetime
from functools import wraps
from flask import Flask, request, jsonify
from werkzeug.wrappers import Request, Response

# Secret key for JWT encoding/decoding
SECRET_KEY = "Open"

class JWTMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            res = Response("Missing or invalid token", mimetype='text/plain', status=401)
            return res(environ, start_response)

        token = auth_header.split("Bearer ")[1]

        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            environ["user"] = decoded_token  # Store user info in environment
        except jwt.ExpiredSignatureError:
            res = Response("Token expired", mimetype='text/plain', status=401)
            return res(environ, start_response)
        except jwt.InvalidTokenError:
            res = Response("Invalid token", mimetype='text/plain', status=401)
            return res(environ, start_response)

        return self.app(environ, start_response)

app = Flask(__name__)
app.wsgi_app = JWTMiddleware(app.wsgi_app)

# Function to generate JWT token (for testing)
def generate_token(username):
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@app.route("/")
def home():
    user = request.environ.get("user", {})
    return jsonify(message="Hello, {}".format(user.get("username", "Naman")))

@app.route("/generate_token")
def get_token():
    token = generate_token("test_user")
    return jsonify(token=token)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
