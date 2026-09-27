import sqlite3

connection = sqlite3.connect("../expenses.db")
cursor = connection.cursor()

cursor.execute("""
ALTER TABLE expenses
ADD COLUMN user_id INTEGER
""")

connection.commit()
connection.close()

print("user_id column added successfully!")