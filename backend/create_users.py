import sqlite3

connection = sqlite3.connect("../expenses.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")

connection.commit()

print("Users table created successfully!")

connection.close()