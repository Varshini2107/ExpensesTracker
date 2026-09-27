import { useEffect, useState } from "react";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
} from "chart.js";
import { Pie, Bar } from "react-chartjs-2";

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement
);

const API_URL = "http://localhost:5000";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const [csrfToken, setCsrfToken] = useState("");

  // Register
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  // Login
  const [loginUsername, setLoginUsername] = useState("");
  const [loginPassword, setLoginPassword] = useState("");

  // Expenses
  const [expenses, setExpenses] = useState([]);

  const [name, setName] = useState("");
  const [category, setCategory] = useState("");
  const [amount, setAmount] = useState("");

  // Get CSRF token when app starts
  useEffect(() => {
    fetch(`${API_URL}/csrf-token`, {
      credentials: "include",
    })
      .then(async (response) => {
        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message || "Could not get CSRF token");
        }

        return data;
      })
      .then((data) => {
        setCsrfToken(data.csrf_token);
      })
      .catch((error) => {
        console.error("CSRF token error:", error);
      });
  }, []);

  // Check existing login session
  useEffect(() => {
    fetch(`${API_URL}/me`, {
      credentials: "include",
    })
      .then(async (response) => {
        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message);
        }

        return data;
      })
      .then((data) => {
        setCurrentUser(data);
        setIsLoggedIn(true);
      })
      .catch(() => {
        setCurrentUser(null);
        setIsLoggedIn(false);
      });
  }, []);

  // Fetch expenses after login
  useEffect(() => {
    if (isLoggedIn) {
      fetchExpenses();
    }
  }, [isLoggedIn]);

  // Get expenses
  function fetchExpenses() {
    fetch(`${API_URL}/expenses`, {
      credentials: "include",
    })
      .then(async (response) => {
        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message);
        }

        return data;
      })
      .then((data) => {
        setExpenses(data);
      })
      .catch((error) => {
        console.error("Error fetching expenses:", error);
      });
  }

  // Register
  function registerUser(event) {
    event.preventDefault();

    const userData = {
      username: username,
      password: password,
    };

    fetch(`${API_URL}/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      credentials: "include",
      body: JSON.stringify(userData),
    })
      .then(async (response) => {
        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message);
        }

        return data;
      })
      .then((data) => {
        alert(data.message);

        setUsername("");
        setPassword("");
      })
      .catch((error) => {
        alert(error.message);
      });
  }

  // Login
  function loginUser(event) {
    event.preventDefault();

    const loginData = {
      username: loginUsername,
      password: loginPassword,
    };

    fetch(`${API_URL}/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      credentials: "include",
      body: JSON.stringify(loginData),
    })
      .then(async (response) => {
        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message);
        }

        return data;
      })
      .then(async (data) => {
        alert(data.message);

        const response = await fetch(`${API_URL}/me`, {
          credentials: "include",
        });

        const userData = await response.json();

        if (!response.ok) {
          throw new Error(userData.message);
        }

        setCurrentUser(userData);
        setIsLoggedIn(true);

        setLoginUsername("");
        setLoginPassword("");
      })
      .catch((error) => {
        alert(error.message);
      });
  }

  // Add expense
  function addExpense(event) {
    event.preventDefault();

    const newExpense = {
      name: name,
      category: category,
      amount: Number(amount),
      date: new Date().toISOString().split("T")[0],
    };

    fetch(`${API_URL}/expenses`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      credentials: "include",
      body: JSON.stringify(newExpense),
    })
      .then(async (response) => {
        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message);
        }

        return data;
      })
      .then((data) => {
        alert(data.message);

        setName("");
        setCategory("");
        setAmount("");

        fetchExpenses();
      })
      .catch((error) => {
        console.error("Error adding expense:", error);
        alert(error.message);
      });
  }

  // Edit expense
  function editExpense(expense) {
    const newName = prompt("Enter expense name:", expense.name);
    const newCategory = prompt("Enter category:", expense.category);
    const newAmount = prompt("Enter amount:", expense.amount);

    if (!newName || !newCategory || !newAmount) {
      return;
    }

    const updatedExpense = {
      name: newName,
      category: newCategory,
      amount: Number(newAmount),
    };

    fetch(`${API_URL}/expenses/${expense.id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      credentials: "include",
      body: JSON.stringify(updatedExpense),
    })
      .then(async (response) => {
        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message);
        }

        return data;
      })
      .then((data) => {
        alert(data.message);
        fetchExpenses();
      })
      .catch((error) => {
        console.error("Error updating expense:", error);
        alert(error.message);
      });
  }

  // Delete expense
  function deleteExpense(id) {
    const confirmDelete = window.confirm(
      "Are you sure you want to delete this expense?"
    );

    if (!confirmDelete) {
      return;
    }

    fetch(`${API_URL}/expenses/${id}`, {
      method: "DELETE",
      headers: {
        "X-CSRFToken": csrfToken,
      },
      credentials: "include",
    })
      .then(async (response) => {
        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message);
        }

        return data;
      })
      .then((data) => {
        alert(data.message);
        fetchExpenses();
      })
      .catch((error) => {
        console.error("Error deleting expense:", error);
        alert(error.message);
      });
  }

  // Logout
  function logout() {
    fetch(`${API_URL}/logout`, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
      },
      credentials: "include",
    })
      .then(async (response) => {
        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message);
        }

        return data;
      })
      .then((data) => {
        alert(data.message);

        setIsLoggedIn(false);
        setCurrentUser(null);
        setExpenses([]);
      })
      .catch((error) => {
        console.error("Logout error:", error);
        alert(error.message);
      });
  }

  // Total spending
  const totalSpending = expenses.reduce(
    (total, expense) => total + Number(expense.amount),
    0
  );

  // Category-wise spending
  const categoryTotals = {};

  expenses.forEach((expense) => {
    if (categoryTotals[expense.category]) {
      categoryTotals[expense.category] += Number(expense.amount);
    } else {
      categoryTotals[expense.category] = Number(expense.amount);
    }
  });

  // Monthly spending
  const monthlyTotals = {};

  expenses.forEach((expense) => {
    if (!expense.date) {
      return;
    }

    const month = expense.date.substring(0, 7);

    if (monthlyTotals[month]) {
      monthlyTotals[month] += Number(expense.amount);
    } else {
      monthlyTotals[month] = Number(expense.amount);
    }
  });

  // Pie chart
  const pieChartData = {
    labels: Object.keys(categoryTotals),
    datasets: [
      {
        label: "Spending",
        data: Object.values(categoryTotals),
        backgroundColor: [
          "#FF6384",
          "#36A2EB",
          "#FFCE56",
          "#4BC0C0",
          "#9966FF",
          "#FF9F40",
        ],
        borderColor: "#ffffff",
        borderWidth: 2,
      },
    ],
  };

  // Bar chart
  const barChartData = {
    labels: Object.keys(monthlyTotals),
    datasets: [
      {
        label: "Monthly Spending",
        data: Object.values(monthlyTotals),
        backgroundColor: "#36eb82",
        borderColor: "#1ee53f",
        borderWidth: 1,
      },
    ],
  };

  return (
    <div className="app">
      <header>
        <h1>💰 Expense Tracker</h1>
        <p>Manage your expenses easily</p>
      </header>

      <main>
        {!isLoggedIn ? (
          <>
            {/* Login */}
            <section className="form-card">
              <h2>Login</h2>

              <form onSubmit={loginUser}>
                <input
                  type="text"
                  placeholder="Username"
                  value={loginUsername}
                  onChange={(event) =>
                    setLoginUsername(event.target.value)
                  }
                  required
                />

                <input
                  type="password"
                  placeholder="Password"
                  value={loginPassword}
                  onChange={(event) =>
                    setLoginPassword(event.target.value)
                  }
                  required
                />

                <button type="submit">Login</button>
              </form>
            </section>

            {/* Register */}
            <section className="form-card">
              <h2>Create Account</h2>

              <form onSubmit={registerUser}>
                <input
                  type="text"
                  placeholder="Username"
                  value={username}
                  onChange={(event) => setUsername(event.target.value)}
                  required
                />

                <input
                  type="password"
                  placeholder="Password"
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  required
                />

                <button type="submit">Register</button>
              </form>
            </section>
          </>
        ) : (
          <>
            {/* Welcome */}
            <section className="dashboard-card">
              <h2>
                Welcome, {currentUser.username}! 👋
              </h2>

              <button onClick={logout}>Logout</button>
            </section>

            {/* Summary */}
            <div className="summary-grid">
              <section className="summary-card total-card">
                <h2>💰 Total Spending</h2>
                <h3>₹{totalSpending.toFixed(2)}</h3>
              </section>

              <section className="summary-card category-card">
                <h2>📂 Categories</h2>
                <h3>{Object.keys(categoryTotals).length}</h3>
                <p>Categories used</p>
              </section>

              <section className="summary-card month-card">
                <h2>📅 This Month</h2>
                <h3>
                  ₹
                  {monthlyTotals[
                    new Date().toISOString().substring(0, 7)
                  ]?.toFixed(2) || "0.00"}
                </h3>
              </section>
            </div>

            {/* Category Spending */}
            <section className="dashboard-card">
              <h2>Category-wise Spending</h2>

              {Object.keys(categoryTotals).length === 0 ? (
                <p>No category data available.</p>
              ) : (
                Object.entries(categoryTotals).map(
                  ([category, total]) => (
                    <div key={category}>
                      <p>
                        <strong>{category}</strong>
                      </p>
                      <p>₹{total.toFixed(2)}</p>
                    </div>
                  )
                )
              )}
            </section>

            {/* Pie Chart */}
            <section className="dashboard-card">
              <h2>Spending by Category</h2>

              {Object.keys(categoryTotals).length === 0 ? (
                <p>No data available for chart.</p>
              ) : (
                <div
                  style={{
                    maxWidth: "500px",
                    margin: "0 auto",
                  }}
                >
                  <Pie data={pieChartData} />
                </div>
              )}
            </section>

            {/* Monthly Spending */}
            <section className="dashboard-card">
              <h2>Monthly Spending</h2>

              {Object.keys(monthlyTotals).length === 0 ? (
                <p>No monthly data available.</p>
              ) : (
                Object.entries(monthlyTotals).map(
                  ([month, total]) => (
                    <div key={month}>
                      <p>
                        <strong>{month}</strong>
                      </p>
                      <p>₹{total.toFixed(2)}</p>
                    </div>
                  )
                )
              )}
            </section>

            {/* Monthly Chart */}
            <section className="dashboard-card">
              <h2>Monthly Spending Chart</h2>

              {Object.keys(monthlyTotals).length === 0 ? (
                <p>No data available for chart.</p>
              ) : (
                <div
                  style={{
                    maxWidth: "700px",
                    margin: "0 auto",
                  }}
                >
                  <Bar data={barChartData} />
                </div>
              )}
            </section>

            {/* Add Expense */}
            <section className="form-card">
              <h2>Add Expense</h2>

              <form onSubmit={addExpense}>
                <input
                  type="text"
                  placeholder="Expense name"
                  value={name}
                  onChange={(event) => setName(event.target.value)}
                  required
                />

                <input
                  type="text"
                  placeholder="Category"
                  value={category}
                  onChange={(event) =>
                    setCategory(event.target.value)
                  }
                  required
                />

                <input
                  type="number"
                  placeholder="Amount"
                  value={amount}
                  onChange={(event) =>
                    setAmount(event.target.value)
                  }
                  required
                />

                <button type="submit">Add Expense</button>
              </form>
            </section>

            {/* Expense List */}
            <section>
              <h2>My Expenses</h2>

              {expenses.length === 0 ? (
                <p>No expenses found.</p>
              ) : (
                <div className="expense-list">
                  {expenses.map((expense) => (
                    <div
                      className="expense-card"
                      key={expense.id}
                    >
                      <div>
                        <h3>{expense.name}</h3>

                        <p>
                          Category: {expense.category}
                        </p>
                      </div>

                      <div>
                        <strong>
                          ₹{Number(expense.amount).toFixed(2)}
                        </strong>

                        <p>
                          {expense.date || "No date"}
                        </p>

                        <button
                          onClick={() =>
                            editExpense(expense)
                          }
                        >
                          Edit
                        </button>

                        <button
                          onClick={() =>
                            deleteExpense(expense.id)
                          }
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </section>
          </>
        )}
      </main>
    </div>
  );
}

export default App;