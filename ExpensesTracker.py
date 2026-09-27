import sqlite3
from datetime import date


def add_expense():
    print("\n===== ADD EXPENSE =====")

    name = input("Enter expense name: ")
    category = input("Enter category: ")

    while True:
        try:
            amount = float(input("Enter amount: "))

            if amount <= 0:
                print("Amount must be greater than 0.")
            else:
                break

        except ValueError:
            print("Please enter a valid amount.")

    # Get today's date
    expense_date = date.today().isoformat()

    # Connect to database
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    # Insert expense with date
    cursor.execute(
        """
        INSERT INTO expenses (name, category, amount, date)
        VALUES (?, ?, ?, ?)
        """,
        (name, category, amount, expense_date)
    )

    connection.commit()
    connection.close()

    print("\nExpense added successfully! ✅")
    print("Date:", expense_date)

def view_expenses():
    print("\n===== ALL EXPENSES =====")

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, name, category, amount, date FROM expenses"
    )

    expenses = cursor.fetchall()

    connection.close()

    if not expenses:
        print("No expenses found.")
        return

    for expense in expenses:
        expense_id = expense[0]
        name = expense[1]
        category = expense[2]
        amount = expense[3]
        expense_date = expense[4]

        print(
            f"{expense_id}. "
            f"{name} | "
            f"{category} | "
            f"₹{amount:.2f} | "
            f"{expense_date}"
        )

def total_spending():
    print("\n===== TOTAL SPENDING =====")

    # Connect to database
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    # Calculate total
    cursor.execute(
        "SELECT SUM(amount) FROM expenses"
    )

    result = cursor.fetchone()

    # Close database
    connection.close()

    if result[0] is None:
        print("No expenses found.")
    else:
        total = result[0]
        print(f"Total Spending: ₹{total:.2f}")
def category_spending():
    print("\n===== CATEGORY SPENDING =====")

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
    """)

    categories = cursor.fetchall()

    connection.close()

    if not categories:
        print("No expenses found.")
        return

    for category in categories:
        name = category[0]
        total = category[1]

        print(f"{name}: ₹{total:.2f}")
def edit_expense():
    print("\n===== EDIT EXPENSE =====")

    expense_id = input("Enter the expense ID to edit: ")

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, name, category, amount FROM expenses WHERE id = ?",
        (expense_id,)
    )

    expense = cursor.fetchone()

    if expense is None:
        print("Expense not found.")
        connection.close()
        return

    print("\nCurrent Expense:")
    print(f"Name: {expense[1]}")
    print(f"Category: {expense[2]}")
    print(f"Amount: ₹{expense[3]:.2f}")

    name = input("Enter new expense name: ")
    category = input("Enter new category: ")
    amount = float(input("Enter new amount: "))

    cursor.execute(
        """
        UPDATE expenses
        SET name = ?, category = ?, amount = ?
        WHERE id = ?
        """,
        (name, category, amount, expense_id)
    )

    connection.commit()
    connection.close()

    print("Expense updated successfully! ✅")
def delete_expense():
    print("\n===== DELETE EXPENSE =====")

    expense_id = input("Enter the expense ID to delete: ")

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, name, category, amount FROM expenses WHERE id = ?",
        (expense_id,)
    )

    expense = cursor.fetchone()

    if expense is None:
        print("Expense not found.")
        connection.close()
        return

    print("\nExpense:")
    print(f"{expense[0]}. {expense[1]} | {expense[2]} | ₹{expense[3]:.2f}")

    confirm = input("Are you sure you want to delete this? (yes/no): ")

    if confirm.lower() == "yes":

        cursor.execute(
            "DELETE FROM expenses WHERE id = ?",
            (expense_id,)
        )

        connection.commit()

        print("Expense deleted successfully! ✅")

    else:
        print("Delete cancelled.")

    connection.close()

while True:

    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Total Spending")
    print("4. Category Spending")
    print("5. Edit Expense")
    print("6. Delete Expense")
    print("7. Exit")
    choice = input("Enter your choice (1-7): ")
    if choice == "1":
        add_expense()
    
    elif choice == "2":
        view_expenses()
    
    elif choice == "3":
        total_spending()
    
    elif choice == "4":
        category_spending()
    
    elif choice == "5":
        edit_expense()
    
    elif choice == "6":
        delete_expense()
    
    elif choice == "7":
        print("\nThank you for using Expense Tracker! 👋")
        break
    
    else:
        print("\n❌ Invalid choice.")
        print("Please enter a number from 1 to 7.")