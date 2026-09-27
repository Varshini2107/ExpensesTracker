from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():
    return "Expense Tracker Backend is Running!"


# =========================================================
# REGISTER
# =========================================================

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data["username"]
    password = data["password"]

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

    username = data["username"]
    password = data["password"]

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

    # Old users have plaintext passwords
    else:
        password_correct = stored_password == password

        # Convert old password to a hash after successful login
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

    if password_correct:
        return jsonify({
            "message": "Login successful!",
            "user_id": user[0],
            "username": user[1]
        }), 200

    return jsonify({
        "message": "Invalid username or password!"
    }), 401
# =========================================================
# GET EXPENSES FOR A USER
# =========================================================

@app.route("/expenses")
def get_expenses():

    user_id = request.args.get("user_id")

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

    data = request.get_json()

    name = data["name"]
    category = data["category"]
    amount = data["amount"]
    expense_date = data["date"]
    user_id = data["user_id"]

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

    data = request.get_json()

    name = data["name"]
    category = data["category"]
    amount = data["amount"]
    user_id = data["user_id"]

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
    data = request.get_json()

    name = data["name"]
    category = data["category"]
    amount = data["amount"]

    connection = sqlite3.connect("../expenses.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE expenses
        SET name = ?, category = ?, amount = ?
        WHERE id = ?
        """,
        (
            name,
            category,
            amount,
            expense_id
        )
    )

    connection.commit()

    connection.close()

    return jsonify({
        "message": "Expense updated successfully!"
    })


# =========================================================
# DELETE EXPENSE
# =========================================================

@app.route("/expenses/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):

    data = request.get_json()

    user_id = data["user_id"]

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
    connection = sqlite3.connect("../expenses.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM expenses
        WHERE id = ?
        """,
        (expense_id,)
    )

    connection.commit()

    connection.close()

    return jsonify({
        "message": "Expense deleted successfully!"
    })


# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)