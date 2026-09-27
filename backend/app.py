from flask import Flask, jsonify, request, session
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
csrf = CSRFProtect(app)
app.secret_key = os.environ.get("SECRET_KEY")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "None"

# Allow React frontend to use the Flask session cookie.
CORS(
    app,
    origins=[
        r"http://localhost:\d+",
        "https://expensestracker-1-p7xx.onrender.com"
    ],
    supports_credentials=True
)
# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():
    return "Expense Tracker Backend is Running!"
@app.route("/csrf-token")
def csrf_token():
    from flask_wtf.csrf import generate_csrf

    return jsonify({
        "csrf_token": generate_csrf()
    })

# =========================================================
# REGISTER
# =========================================================

@app.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "message": "Username and password are required!"
        }), 400

    hashed_password = generate_password_hash(password)

    connection = sqlite3.connect("../expenses.db")
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users (username, password)
            VALUES (?, ?)
            """,
            (username, hashed_password)
        )

        connection.commit()

        return jsonify({
            "message": "User registered successfully!"
        }), 201

    except sqlite3.IntegrityError:

        return jsonify({
            "message": "Username already exists!"
        }), 400

    finally:
        connection.close()


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "message": "Username and password are required!"
        }), 400

    connection = sqlite3.connect("../expenses.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, username, password
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    user = cursor.fetchone()

    if not user:

        connection.close()

        return jsonify({
            "message": "Invalid username or password!"
        }), 401

    stored_password = user[2]

    # New users have hashed passwords
    if stored_password.startswith(("scrypt:", "pbkdf2:")):

        password_correct = check_password_hash(
            stored_password,
            password
        )

    # Old users may still have plaintext passwords
    else:

        password_correct = stored_password == password

        # Convert old password to a hash
        if password_correct:

            hashed_password = generate_password_hash(password)

            cursor.execute(
                """
                UPDATE users
                SET password = ?
                WHERE id = ?
                """,
                (hashed_password, user[0])
            )

            connection.commit()

    connection.close()

    if not password_correct:

        return jsonify({
            "message": "Invalid username or password!"
        }), 401

    # -----------------------------------------------------
    # SERVER-SIDE SESSION
    # -----------------------------------------------------

    session["user_id"] = user[0]
    session["username"] = user[1]

    return jsonify({
        "message": "Login successful!",
        "username": user[1]
    }), 200


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout", methods=["POST"])
def logout():

    session.clear()

    return jsonify({
        "message": "Logged out successfully!"
    }), 200


# =========================================================
# CHECK CURRENT LOGIN
# =========================================================

@app.route("/me")
def current_user():

    if "user_id" not in session:

        return jsonify({
            "message": "Not logged in!"
        }), 401

    return jsonify({
        "user_id": session["user_id"],
        "username": session["username"]
    }), 200


# =========================================================
# GET EXPENSES FOR LOGGED-IN USER
# =========================================================

@app.route("/expenses")
def get_expenses():

    if "user_id" not in session:

        return jsonify({
            "message": "Please login first!"
        }), 401

    user_id = session["user_id"]

    connection = sqlite3.connect("../expenses.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM expenses
        WHERE user_id = ?
        """,
        (user_id,)
    )

    expenses = cursor.fetchall()

    connection.close()

    expense_list = []

    for expense in expenses:
        expense_list.append(dict(expense))

    return jsonify(expense_list)


# =========================================================
# ADD EXPENSE
# =========================================================

@app.route("/expenses", methods=["POST"])
def add_expense():

    if "user_id" not in session:

        return jsonify({
            "message": "Please login first!"
        }), 401

    data = request.get_json()

    name = data.get("name")
    category = data.get("category")
    amount = data.get("amount")
    expense_date = data.get("date")

    if not name or not category or amount is None or not expense_date:

        return jsonify({
            "message": "All expense fields are required!"
        }), 400

    # IMPORTANT:
    # user_id comes from the server session.
    # The client cannot choose another user's ID.
    user_id = session["user_id"]

    connection = sqlite3.connect("../expenses.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO expenses
        (name, category, amount, date, user_id)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            name,
            category,
            amount,
            expense_date,
            user_id
        )
    )

    connection.commit()

    new_id = cursor.lastrowid

    connection.close()

    return jsonify({
        "message": "Expense added successfully!",
        "id": new_id
    }), 201


# =========================================================
# EDIT EXPENSE
# =========================================================

@app.route("/expenses/<int:expense_id>", methods=["PUT"])
def update_expense(expense_id):

    if "user_id" not in session:

        return jsonify({
            "message": "Please login first!"
        }), 401

    data = request.get_json()

    name = data.get("name")
    category = data.get("category")
    amount = data.get("amount")

    if not name or not category or amount is None:

        return jsonify({
            "message": "All expense fields are required!"
        }), 400

    user_id = session["user_id"]

    connection = sqlite3.connect("../expenses.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE expenses
        SET name = ?, category = ?, amount = ?
        WHERE id = ? AND user_id = ?
        """,
        (
            name,
            category,
            amount,
            expense_id,
            user_id
        )
    )

    connection.commit()

    updated = cursor.rowcount

    connection.close()

    if updated == 0:

        return jsonify({
            "message": "Expense not found or does not belong to this user!"
        }), 404

    return jsonify({
        "message": "Expense updated successfully!"
    }), 200


# =========================================================
# DELETE EXPENSE
# =========================================================

@app.route("/expenses/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):

    if "user_id" not in session:

        return jsonify({
            "message": "Please login first!"
        }), 401

    user_id = session["user_id"]

    connection = sqlite3.connect("../expenses.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM expenses
        WHERE id = ? AND user_id = ?
        """,
        (
            expense_id,
            user_id
        )
    )

    connection.commit()

    deleted = cursor.rowcount

    connection.close()

    if deleted == 0:

        return jsonify({
            "message": "Expense not found or does not belong to this user!"
        }), 404

    return jsonify({
        "message": "Expense deleted successfully!"
    }), 200


# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)