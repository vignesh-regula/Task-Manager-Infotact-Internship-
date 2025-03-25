from flask import Flask, render_template, request, session, jsonify, redirect, url_for
import jwt
from datetime import datetime, timedelta
from functools import wraps
import task_manager  # Import the task management functions

app = Flask(__name__)
app.config["SECRET_KEY"] = "8@e345%980yu06!2@004"

# Decorator to protect routes that require a valid token
def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get("token") or request.form.get("token")
        if not token:
            return "Token is missing", 403
        try:
            payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return "Token has expired", 401
        except jwt.InvalidTokenError:
            return "Invalid token", 401
        
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
            token = jwt.encode({"user": name, "exp": datetime.utcnow() + timedelta(seconds=180)},
                               app.config["SECRET_KEY"], algorithm="HS256")
            return render_template("index.html", token=token)
        else:
            return "Invalid credentials", 403
    return render_template('login.html')

@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        task_manager.create_user(username, password)  # Create new user
        return redirect(url_for('pre_index'))  # Redirect to login page after registration
    return render_template("sign.html")

@app.route("/index")
@token_required
def index():
    user_id = session.get("user_id")
    tasks = task_manager.get_all_tasks(user_id)  # Fetch tasks for the logged-in user
    return render_template("index.html", tasks=tasks)

@app.route("/create_task", methods=["POST"])
@token_required
def create_task():
    token = request.form['token']  # Retrieve token from the form
    if not token:
        return "Token is missing", 403
    
    user_id = session.get("user_id")
    title = request.form['title']
    priority = request.form['priority']
    status = request.form['status']
    deadline = request.form['deadline']

    task_manager.create_task(title, priority, status, deadline, user_id)  # Add new task for the user

    token = request.form.get("token")  # Retrieve token from form
    return redirect(url_for('index', token=token))  # Redirect back to the index page


@app.route("/update_task/<int:task_id>", methods=["POST"])
@token_required
def update_task(task_id):
    user_id = session.get("user_id")
    title = request.form['title']
    priority = request.form['priority']
    status = request.form['status']
    deadline = request.form['deadline']

    task_manager.update_task(task_id, title, priority, status, deadline, user_id)  # Update task in DB

    return redirect(url_for('index'))  # Redirect back to the index page

@app.route("/delete_task/<int:task_id>", methods=["POST"])
@token_required
def delete_task(task_id):
    user_id = session.get("user_id")
    task_manager.delete_task(task_id, user_id)  # Delete task from DB

    return redirect(url_for('index'))  # Redirect back to the index page

if __name__ == "__main__":
    app.run(debug=True)
