# AI-Powered Task Management System

## 📌 Project Overview
The **AI-Powered Task Management System** is a **Flask-based** web application designed to enhance **task organization, productivity, and collaboration**. It integrates **JWT-based authentication**, **session management**, and a **MySQL database** for secure user management and task tracking. Future enhancements will include **AI-driven task prioritization and automated scheduling**.

## 🚀 Features Implemented

### 🔐 **User Authentication & Authorization**
- **JWT-Based Authentication**: Secure login and token-based authorization.
- **Session-Based Authentication**: Enhanced security with Flask sessions.
- **Role-Based Access Control**: User roles (Admin, Manager, Employee) with different permissions.
- **Password Hashing**: Secure credential storage.

### 📋 **Task Management System**
- **CRUD Operations**: Users can create, view, update, and delete tasks.
- **Task Categorization**: Tasks prioritized as **Urgent, High, Medium, Low**.
- **Status Tracking**: Task progress tracked as **To-Do, In Progress, Completed, On-Hold**.
- **Deadline & Notifications**: Task due dates with future notification support.
- **User-Based Task Filtering**: Personalized task views for users.

### 🔒 **Security Measures**
- **JWT Token Authentication** for API security.
- **Session Management** to prevent token loss on redirection.
- **Encrypted Password Storage** to prevent unauthorized access.
- **SQL Injection Prevention** with parameterized queries.

## 📂 Project Structure
```
AI_Task_Manager/
├── backend/
│   ├── app.py              # Main Flask Application
│   ├── authentication.py   # User login/signup with JWT & session handling
│   ├── task_manager.py     # Task-related operations
│   ├── database.py         # Database connection & schema
│   ├── models.py           # User & Task models
│   ├── requirements.txt    # Project dependencies
│
├── frontend/
│   ├── templates/
│   │   ├── index.html      # Dashboard UI
│   │   ├── login.html      # Login Page
│   │   ├── signup.html     # Registration Page
│   ├── static/
│   │   ├── styles.css      # CSS Styles
│   │   ├── script.js       # JavaScript for interactivity
│
├── README.md               # Documentation
```

## ⚙️ Installation & Setup
### 1️⃣ **Clone the Repository**
```sh
git clone https://github.com/your-repo/task-manager.git
cd task-manager
```

### 2️⃣ **Set Up a Virtual Environment**
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ **Install Dependencies**
```sh
pip install -r backend/requirements.txt
```

### 4️⃣ **Configure Database**
- Create a **MySQL database**.
- Update `database.py` with database credentials.
- Run the database setup script:
```sh
python backend/database.py
```

### 5️⃣ **Run the Application**
```sh
python backend/app.py
```
Access the application at: **`http://localhost:5000`**

## 🛠️ Future Enhancements
✅ **AI-Powered Task Prioritization** based on sentiment analysis.
✅ **Automated Scheduling & Predictive Analytics**.
✅ **Real-Time Collaboration & Notifications** for task updates.
✅ **Integration with External Tools** like Slack & Google Calendar.

---
💡 Developed with ❤️ using Flask & MySQL 🚀

