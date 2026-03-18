from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)

# Secret key required for sessions
app.secret_key = "supersecretkey"

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)


# -------------------------
# DATABASE MODEL
# -------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.LargeBinary)   # store hashed password
    role = db.Column(db.String(20))
    failed_attempts = db.Column(db.Integer, default=0)
    lock_until = db.Column(db.DateTime, nullable=True)


# -------------------------
# LOGIN ROUTE
# -------------------------
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"].strip()
        password = request.form["password"]
        captcha = request.form["captcha"]

        # CAPTCHA verification
        if captcha != "8":
            return render_template("error.html", message="CAPTCHA verification failed")

        # Check empty fields
        if not email or not password:
            return render_template("error.html", message="Email and password required")

        # Find user by email
        user = User.query.filter_by(email=email).first()

        # If user not found
        if user is None:
            return render_template("error.html", message="Invalid email or password")

        # Check if account is locked
        if user.lock_until and datetime.now() < user.lock_until:
            return render_template("error.html", message="Account locked. Try again later.")

        # Check password
        if not bcrypt.checkpw(password.encode('utf-8'), user.password):

            user.failed_attempts += 1

            if user.failed_attempts >= 3:
                user.lock_until = datetime.now() + timedelta(seconds=30)
                user.failed_attempts = 0

            db.session.commit()

            return render_template("error.html", message="Invalid email or password")

        # Reset attempts after successful login
        user.failed_attempts = 0
        user.lock_until = None
        db.session.commit()

        # Login successful
        session['user_id'] = user.id

        # Role based redirect
        if user.role == "Admin":
            return redirect("/admin")
        else:
            return redirect("/dashboard")

    return render_template("login.html")
# -------------------------
# REGISTER ROUTE
# -------------------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"].strip()
        email = request.form["email"].strip()
        password = request.form["password"]
        role = request.form["role"]

        # 1️ Check empty fields
        if not username or not email or not password:
            return "All fields are required"

        # 2️ Prevent duplicate email
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return render_template("error.html", message="Email already registered")

        # 3️ Basic password strength check
        if len(password) < 6:
           return render_template("error.html", message="Password must be at least 6 characters")

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            role=role
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect("/")

    return render_template("register.html")
# -------------------------
# USER DASHBOARD
# -------------------------
@app.route("/dashboard")
def dashboard():

    if 'user_id' not in session:
        return redirect("/")

    return render_template("dashboard.html")


# -------------------------
# ADMIN PANEL
# -------------------------
@app.route("/admin")
def admin():

    if 'user_id' not in session:
        return redirect("/")

    user = User.query.get(session['user_id'])

    if user.role != "Admin":
        return "Access Denied"

    users = User.query.all()

    return render_template("admin.html", users=users)

@app.route("/delete_user/<int:user_id>")
def delete_user(user_id):

    if 'user_id' not in session:
        return redirect("/")

    admin_user = User.query.get(session['user_id'])

    if admin_user is None:
        return redirect("/")

    if admin_user.role != "Admin":
        return "Access Denied"

    user_to_delete = User.query.get(user_id)

    if user_to_delete:

        if user_to_delete.id == admin_user.id:
           return render_template("error.html", message="Admin cannot delete himself")

        db.session.delete(user_to_delete)
        db.session.commit()

    return redirect("/admin")

# -------------------------
# LOGOUT
# -------------------------
@app.route("/logout")
def logout():
    session.pop('user_id', None)
    return redirect("/")


# -------------------------
# RUN APP
# -------------------------
if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)