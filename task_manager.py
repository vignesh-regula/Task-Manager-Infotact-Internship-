import mysql.connector,os
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
# Database connection setup

load_dotenv()
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# Create a new user (with hashed password)
def create_user(username, password):
    connection = get_db_connection()
    cursor = connection.cursor()

    password_hash = generate_password_hash(password)

    cursor.execute("""
        INSERT INTO users (username, password_hash)
        VALUES (%s, %s)
    """, (username, password_hash))

    connection.commit()
    cursor.close()
    connection.close()

# Check user credentials for login
def check_user_credentials(username, password):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if user and check_password_hash(user[2], password):  # user[2] is password_hash
        return user  # Returns user data if credentials are correct
    return None

# Create a new task for a specific user
def create_task(title, priority, status, deadline, user_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO tasks (title, priority, status, deadline, user_id)
        VALUES (%s, %s, %s, %s, %s)
    """, (title, priority, status, deadline, user_id))

    connection.commit()
    cursor.close()
    connection.close()

# Get all tasks for a specific user
def get_all_tasks(user_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
    tasks = cursor.fetchall()

    cursor.close()
    connection.close()

    return tasks

# Update a task
def update_task(task_id, title, priority, status, deadline, user_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE tasks
        SET title = %s, priority = %s, status = %s, deadline = %s
        WHERE id = %s AND user_id = %s
    """, (title, priority, status, deadline, task_id, user_id))

    connection.commit()
    cursor.close()
    connection.close()

# Delete a task
def delete_task(task_id, user_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM tasks WHERE id = %s AND user_id = %s", (task_id, user_id))

    connection.commit()
    cursor.close()
    connection.close()
