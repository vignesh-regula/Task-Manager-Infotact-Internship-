from flask import Flask, render_template, request, session, jsonify, make_response
from functools import wraps
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)

# Corrected SECRET_KEY
app.config["SECRET_KEY"] = "8@e345%980yu06!2@004"

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get("token")
        if not token:
            return "Token is missing", 403
        try:
            payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return "Token has expired", 401
        except jwt.InvalidTokenError:
            return "Invalid token", 401
        # You can add payload or user information to `session` or pass as a variable here
        return func(*args, **kwargs)  # Call the original function
    return decorated


@app.route("/", methods=["GET", "POST"])
def pre_index():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        if name and password == "123":
            session["logged_in"] = True
            token = jwt.encode({"user": name, "exp": datetime.utcnow() + timedelta(seconds=180)},
                               app.config["SECRET_KEY"], algorithm="HS256")
            return render_template("index.html", token=token)
        else:
            return "Invalid credentials", 403  # You can also redirect to login
    return render_template('login.html')


@app.route("/signup")
def sign_up():
    return render_template("sign.html")


@app.route("/index")
@token_required
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
