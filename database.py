import sqlite3


def create_database():
    connection = sqlite3.connect("expenses.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL
        )
    """)

    connection.commit()
    connection.close()

    print("Database created successfully!")


create_database()