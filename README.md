# 💰 Expense Tracker

A full-stack Expense Tracker web application built using **React, Flask, and SQLite**.

The application allows users to register, log in, and manage their personal expenses. Users can add, edit, delete, and view expenses along with spending summaries and charts.

## 🚀 Features

- 👤 User registration and login
- 🔐 Password hashing
- ➕ Add expenses
- ✏️ Edit expenses
- 🗑️ Delete expenses
- 📋 View personal expenses
- 💰 Calculate total spending
- 📂 Category-wise spending
- 📅 Monthly spending summary
- 📊 Spending visualization using charts
- 🗄️ SQLite database
- 🌐 React frontend
- ⚙️ Flask backend
- 🔗 REST API communication

## 🛠️ Technologies Used

### Frontend

- React.js
- Vite
- JavaScript
- HTML
- CSS
- Chart.js
- React Chart.js 2

### Backend

- Python
- Flask
- Flask-CORS
- SQLite
- Werkzeug

### Tools

- Git
- GitHub
- VS Code

## 📁 Project Structure

```text
ExpenseTracker/
│
├── ExpensesTracker.py
├── database.py
├── update_database.py
├── .gitignore
├── README.md
│
├── backend/
│   ├── app.py
│   ├── create_users.py
│   ├── add_user_id.py
│   ├── test_api.py
│   ├── test_login.py
│   ├── test_register.py
│   └── venv/
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
└── screenshots/
    ├── login-register.png
    ├── dashboard-summary.png
    ├── category-chart.png
    ├── monthly-chart.png
    └── my-expenses.png