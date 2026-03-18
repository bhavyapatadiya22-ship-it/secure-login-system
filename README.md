# Secure Login System with User Role Management

## Introduction

This project is a simple web-based login system developed using **Python Flask and SQLite**.
The purpose of this project is to demonstrate how a secure authentication system works and how different user roles can be managed in a web application.

The system allows users to register, login, and access different dashboards depending on their role (Admin or User).

This project was created as part of a **Cybersecurity Internship** to practice secure authentication, access control, and basic security enhancements in a web environment.

---

# Technologies Used

The following technologies were used to build this project:

* Python
* Flask (Web Framework)
* SQLite (Database)
* SQLAlchemy (ORM for database operations)
* bcrypt (Password hashing)
* HTML
* CSS

---

# Project Features

## User Registration

Users can create a new account using the registration page.

During registration the user must provide:

* Username
* Email
* Password
* Role (Admin or User)

Passwords are **not stored as plain text**.
They are securely hashed using **bcrypt** before being saved in the database.

---

## Secure Login System

Users can log in using their registered email and password.

The system verifies:

1. Whether the email exists in the database.
2. Whether the entered password matches the hashed password stored in the database.

If authentication is successful, the user is redirected to the appropriate dashboard.

---

## Session-Based Authentication

The application uses **Flask sessions** to maintain the login state of users.

After successful login, a session is created to keep the user authenticated during their interaction with the system.

This prevents unauthorized access to protected pages.

---

## Role-Based Access Control (RBAC)

The system supports two user roles:

* Admin
* User

After login:

* **Admin users** are redirected to the **Admin Dashboard**
* **Normal users** are redirected to the **User Dashboard**

This ensures that users can only access the features allowed for their role.

---

## Admin Dashboard

The Admin Dashboard allows administrators to view all registered users.

The dashboard displays:

* User ID
* Username
* Email
* Role

This helps the administrator manage the system users easily.

---

## User Management

Admin users have the ability to **delete user accounts** from the system.

Each user in the admin dashboard has a **Delete option** which removes that user from the database.

---

## Important Security Rule

The system includes an important security rule:

**An admin cannot delete their own account.**

This prevents accidental loss of administrator access and ensures that the system always retains administrative control.

---

# Security Enhancements 

Additional security mechanisms were implemented to protect the system from common cyber attacks.

## SQL Injection Protection

The project uses **SQLAlchemy ORM** instead of raw SQL queries.

ORM automatically handles parameterized queries, which prevents malicious SQL code from being injected into the application.

This protects the database from **SQL Injection attacks**.

---

## CAPTCHA Verification

A simple CAPTCHA verification was added to the login page to prevent automated login attempts.

Users must answer a small math question before logging in.

Example:

3 + 5 = ?

If the CAPTCHA answer is incorrect, the login request will be rejected and an error message will be displayed.

This helps prevent **bot-based login attempts**.

---

## Account Lockout Protection

To protect the system from **brute-force password attacks**, a login attempt monitoring mechanism was implemented.

Security behavior:

* The system tracks failed login attempts.
* After **3 incorrect password attempts**, the user account becomes temporarily locked.
* The account automatically unlocks after **30 seconds**.

This prevents attackers from repeatedly trying multiple passwords to gain unauthorized access.

---

# User Interface Styling (CSS)

Basic CSS styling was added to improve the visual appearance of the web application.

UI improvements include:

* Navy blue background theme with white text
* Login and registration forms centered on the page
* Styled input fields and buttons
* Reusable container layout for consistent design
* Centered admin dashboard table

A single global stylesheet (`style.css`) is used across all pages to maintain a consistent user interface.

---

# Project Structure

secure-login-system

app.py
README.md
.gitignore

templates/
login.html
register.html
dashboard.html
admin.html
error.html

static/
style.css

instance/
users.db

---

# How to Run the Project

Follow these steps to run the project locally.

## Step 1 – Install Required Libraries

Install the required Python packages:

pip install flask flask_sqlalchemy bcrypt

---

## Step 2 – Run the Application

Start the Flask server using:

python app.py

---

## Step 3 – Open the Application

Open your browser and visit:

http://127.0.0.1:5000

---

# Example Test Accounts

Example accounts can be created through the registration page.

Example:

Admin Account
Email: [admin@test.com](mailto:admin@test.com)
Password: admin123
Role: Admin

User Account
Email: [user@test.com](mailto:user@test.com)
Password: user123
Role: User

---

# What I Learned From This Project

While building this project, I learned:

* How authentication systems work
* How to securely store passwords using hashing
* How to implement role-based access control
* How to build an admin dashboard for managing users
* How to apply security mechanisms such as CAPTCHA and account lockout
* How to improve web interface design using CSS

---

# Conclusion

This project demonstrates a beginner-friendly implementation of a **secure login system using Flask**.

It includes authentication, password hashing, role-based access control, an admin dashboard for user management, and multiple security enhancements such as CAPTCHA verification and account lockout protection.

The project helped in understanding the fundamentals of **secure user authentication and web application security**.
