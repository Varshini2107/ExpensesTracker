import sqlite3

connection = sqlite3.connect("expenses.db")
cursor = connection.cursor()

cursor.execute("""
    ALTER TABLE expenses
    ADD COLUMN date TEXT
""")

connection.commit()
connection.close()

print("Database updated successfully!")