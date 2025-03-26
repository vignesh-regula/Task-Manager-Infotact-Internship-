from flask import Flask, render_template, request, session, jsonify, redirect, url_for, make_response
import jwt
import os
from datetime import datetime, timedelta
from functools import wraps
import task_manager  # Import task management functions
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Decorator to protect routes that require authentication
def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.cookies.get("token")  # ✅ Read token from HTTP-Only cookie
        
        if not token:
            return jsonify({"message": "Token is missing"}), 403
        
        try:
            payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            session["user_id"] = payload["user_id"]  # Store user ID in session
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401

        return func(*args, **kwargs)

    return decorated

@app.route("/", methods=["GET", "POST"])
def pre_index():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        
        user = task_manager.check_user_credentials(name, password)
        if user:
            session["logged_in"] = True
            session["user_id"] = user[0]  # Store user_id in session
            
            # Generate JWT Token
            token = jwt.encode(
                {"user_id": user[0], "exp": datetime.utcnow() + timedelta(hours=1)},
                app.config["SECRET_KEY"],
                algorithm="HS256"
            )

            response = make_response(redirect(url_for("index")))
            response.set_cookie("token", token, httponly=True, secure=True, samesite="Strict")  # ✅ Store token in HTTP-Only Cookie
            return response

        return "Invalid credentials", 403
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        task_manager.create_user(username, password)  # Create new user
        return redirect(url_for('pre_index'))  # Redirect to login page after registration
    return render_template("signup.html")

@app.route("/logout")
def logout():
    response = make_response(redirect(url_for("pre_index")))
    response.set_cookie("token", "", expires=0)  # ✅ Clear the token on logout
    return response

@app.route("/index")
@token_required
def index():
    user_id = session.get("user_id")
    tasks = task_manager.get_all_tasks(user_id)  # Fetch tasks for the logged-in user
    return render_template("index.html", tasks=tasks)

@app.route("/create_task", methods=["POST"])
@token_required
def create_task():
    user_id = session.get("user_id")
    title = request.form['title']
    priority = request.form['priority']
    status = request.form['status']
    deadline = request.form['deadline']

    task_manager.create_task(title, priority, status, deadline, user_id)  # Add new task for the user
    return redirect(url_for('index'))  

@app.route("/update_task/<int:task_id>", methods=["POST"])
@token_required
def update_task(task_id):
    user_id = session.get("user_id")
    title = request.form['title']
    priority = request.form['priority']
    status = request.form['status']
    deadline = request.form['deadline']

    task_manager.update_task(task_id, title, priority, status, deadline, user_id)  # Update task in DB
    return redirect(url_for('index'))  

@app.route("/delete_task/<int:task_id>", methods=["POST"])
@token_required
def delete_task(task_id):
    user_id = session.get("user_id")
    task_manager.delete_task(task_id, user_id)  # Delete task from DB
    return redirect(url_for('index'))  

if __name__ == "__main__":
    app.run(debug=True)
