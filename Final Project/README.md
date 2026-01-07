# 💰 Personal Finance Tracker

#### Video Demo: https://www.youtube.com/watch?v=T7xxLrjQzPQ

#### Description:

Personal Finance Tracker is a full-stack web application designed to help users manage their personal finances effectively. The application allows users to register, log in securely, track their income and expenses, and visualize their financial data through interactive charts. It's built with a focus on simplicity, security, and user experience.

## Project Overview

This project demonstrates a complete full-stack web development workflow using Python, Flask, SQLite, and vanilla JavaScript. It showcases user authentication, database design and management, RESTful API development, and responsive frontend design.

### Core Problem Solved

Managing personal finances can be overwhelming. Many people struggle to track where their money goes, what categories they spend most on, and whether they're staying within their means. This application provides a simple, intuitive interface to log transactions and visualize spending patterns at a glance.

### Why This Approach?

I chose this tech stack because:
- **Flask** is lightweight and perfect for rapid development without unnecessary overhead
- **SQLite** provides file-based persistence, ideal for a personal app (no database server needed)
- **Vanilla JavaScript** keeps the project lightweight and removes dependencies on heavy frameworks
- **Chart.js** provides beautiful, responsive charts with minimal configuration
- This combination is beginner-friendly yet demonstrates professional development practices

## File Structure & Explanation

### Backend Files

**`app.py` (Main Application - 250+ lines)**

This is the core of the application. It contains:

1. **Flask Setup**: Initializes the Flask app with secret key for session management
2. **Database Connection**: `get_db_connection()` function establishes SQLite connections
3. **Database Initialization**: `init_db()` creates tables if they don't exist (users and transactions)
4. **Authentication Routes**:
   - `/register` - Handles user registration with password validation
   - `/login` - Validates credentials and creates sessions
   - `/logout` - Clears user session
5. **Dashboard Route**: `/` - Main dashboard (protected, requires login)
6. **Transaction APIs**:
   - `POST /api/add-transaction` - Creates new transaction with validation
   - `GET /api/get-transactions` - Retrieves all user transactions
   - `GET /api/get-balance` - Calculates current balance
   - `DELETE /api/delete-transaction/<id>` - Removes transactions
   - `GET /api/get-chart-data` - Aggregates data for charts

**Design Choices in app.py:**
- Used **Werkzeug's `generate_password_hash` and `check_password_hash`** for secure password storage (never storing plaintext)
- Implemented **user isolation**: Each query filters by `user_id` to ensure users only see their data
- Used **SQLite Row factory** for clean object-like access to database results
- Built **REST API endpoints** that return JSON, enabling easy frontend communication
- Added **input validation** on all endpoints to prevent invalid data

**`requirements.txt`**

Contains project dependencies:
- Flask 2.3.2 - Web framework
- Werkzeug 2.3.6 - Security utilities for password hashing

### Frontend Files

**`templates/login.html` (40 lines)**

The login page with:
- Form for username and password
- Error messages for failed authentication
- Link to registration page
- Success message after registration

**`templates/register.html` (45 lines)**

User registration form with:
- Username and password inputs
- Password confirmation field
- Validation for minimum 6 characters
- Error handling for duplicate usernames

**`templates/index.html` (100+ lines)**

The main dashboard containing:
- Navigation bar with logout button
- Overview cards showing total balance, income, and expenses
- Transaction form with type, amount, category, date, and notes fields
- Two interactive charts (expense pie chart, balance line chart)
- Transactions table with filtering and delete functionality

**`static/style.css` (400+ lines)**

Comprehensive CSS styling including:
- Responsive grid layouts using CSS Grid
- Flexbox for navigation and form layouts
- Mobile-first responsive design (breakpoints at 768px and 480px)
- Color scheme with CSS custom properties (--primary-color, --secondary-color, etc.)
- Smooth transitions and hover effects
- Dark border accents for card styling
- Table styling with alternating row effects

**Design Choices in CSS:**
- Used **CSS Custom Properties (variables)** for consistent theming
- Implemented **CSS Grid** for responsive layouts that adapt to screen size
- Used **flexbox** for navigation and form alignment
- Mobile-first approach ensures the design works on all devices
- Semantic color choices (green for income, red for expenses)

**`static/chart.js` (300+ lines)**

Vanilla JavaScript handling:
- Transaction form submission with validation
- API calls to backend using `fetch()`
- Real-time data loading and display
- Chart rendering using Chart.js library
- Transaction filtering by category and type
- Delete functionality with confirmation
- Auto-refresh data every 30 seconds
- Currency formatting for display

**Design Choices in JavaScript:**
- Used **vanilla JavaScript** instead of frameworks for lighter weight
- Implemented **event delegation** for dynamic transaction rows
- Used **async/await** for clean asynchronous code
- **Client-side validation** before sending to server
- Global variable `allTransactions` caches data for efficient filtering
- Chart instances stored to allow destruction/recreation on data updates

## Features

### Core Features ✅
- **User Authentication**: Secure registration and login with password hashing using Werkzeug
- **Add Transactions**: Record income or expense with amount, category, date, and optional notes
- **View Transactions**: Table display of all transactions with sorting by date
- **Filter Transactions**: Real-time filtering by category name and transaction type
- **Balance Display**: Real-time calculation of total balance, total income, and total expenses
- **Interactive Charts**:
  - Doughnut chart showing expense breakdown by category
  - Line chart displaying balance trend over time
- **Transaction Management**: Delete transactions with confirmation dialog
- **Responsive Design**: Fully responsive UI for desktop, tablet, and mobile devices
- **Session Management**: Secure user sessions with automatic logout

### Design Decisions

1. **SQLite over other databases**: SQLite is perfect for personal projects as it requires no server setup and stores everything in a single file
2. **Vanilla JavaScript**: Chose not to use React/Vue to keep the project lightweight and focused on core concepts
3. **Charts.js**: Simple yet powerful charting library that doesn't require configuration
4. **Simple categorization**: Instead of predefined categories, users can create custom categories for flexibility
5. **Soft delete consideration**: Currently hard-deletes transactions; could be soft-delete for audit trails
6. **Real-time auto-refresh**: Charts and balance update every 30 seconds without page reload for better UX

### Future Enhancement Opportunities 🚀
- Export transactions to CSV
- Monthly budget limits with alerts when exceeded
- Recurring transaction templates
- Data import from bank statements
- Advanced analytics (year-over-year comparisons)
- Dark mode toggle
- Multi-currency support
- Spending goals with progress tracking
- Email notifications for large expenses
- Data encryption at rest

## Tech Stack & Justification

| Layer | Technology | Why? |
|-------|-----------|------|
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla) | Clean, no dependencies, demonstrates core web skills |
| **Backend** | Python with Flask | Lightweight, perfect for learning, rapid development |
| **Database** | SQLite | File-based, zero setup, perfect for personal projects |
| **Charts** | Chart.js | Minimal configuration, beautiful output, responsive |
| **Security** | Werkzeug | Industry-standard password hashing, prevents common attacks |

## Project Structure

```
project/
├── app.py                    # Flask application & API routes
├── finance.db               # SQLite database (auto-created)
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── templates/
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   └── index.html          # Dashboard
└── static/
    ├── style.css           # CSS styling
    └── chart.js            # JavaScript for charts & transactions
```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
);
```

### Transactions Table
```sql
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    type TEXT NOT NULL,           -- 'income' or 'expense'
    amount REAL NOT NULL,
    category TEXT,
    date TEXT NOT NULL,
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Clone/Download the Project
```bash
cd path/to/project
```

### Step 2: Create a Virtual Environment (Recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python app.py
```

The app will start at `http://localhost:5000`

## Usage

### 1. Create an Account
- Click "Register here" on the login page
- Choose a username and password (min 6 characters)
- Confirm your password and register

### 2. Log In
- Enter your username and password
- You'll be redirected to the dashboard

### 3. Add Transactions
- Fill in the transaction form:
  - **Type**: Select "Income" or "Expense"
  - **Amount**: Enter the transaction amount
  - **Category**: Choose or create a category (e.g., "Salary", "Food", "Rent")
  - **Date**: Select the transaction date
  - **Notes**: (Optional) Add any notes
- Click "Add Transaction"

### 4. View & Manage Transactions
- All transactions appear in the table below
- Use the **Category Filter** to search by category name
- Use the **Type Filter** to show only income or expenses
- Click "Delete" to remove a transaction (confirmation required)

### 5. Review Charts
- **Expenses by Category**: Pie chart showing spending distribution
- **Balance Over Time**: Line chart showing account balance changes

### 6. Check Your Balance
- Total balance, income, and expenses are displayed at the top of the dashboard
- Updates automatically as you add/delete transactions

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Register a new user |
| POST | `/login` | Log in a user |
| GET | `/logout` | Log out the current user |
| POST | `/api/add-transaction` | Add a new transaction |
| GET | `/api/get-transactions` | Get all transactions for user |
| GET | `/api/get-balance` | Get balance info |
| GET | `/api/get-chart-data` | Get data for charts |
| DELETE | `/api/delete-transaction/<id>` | Delete a transaction |

## Security Features

✅ **Password Hashing**: Passwords are hashed using Werkzeug security
✅ **Session Management**: User sessions are maintained securely
✅ **CSRF Protection**: Forms validated on the backend
✅ **User Isolation**: Each user only sees their own data
✅ **Input Validation**: All inputs are validated before processing

## Key Technologies Explained

### Flask
Lightweight Python web framework for handling routes and requests.

### SQLite
File-based database, perfect for small projects. No server setup needed.

### Chart.js
JavaScript library for creating beautiful, responsive charts.

### Werkzeug
Provides security utilities for password hashing and verification.

## Future Enhancements

1. **CSV Export**: Download transactions as CSV file
2. **Monthly Budgets**: Set spending limits per category
3. **Budget Alerts**: Get notified when exceeding budget
4. **Recurring Transactions**: Automate regular payments
5. **Advanced Analytics**: Year-over-year comparisons
6. **Dark Mode**: Theme switcher for user preference
7. **Multi-currency**: Support for different currencies
8. **Spending Goals**: Set and track savings goals
9. **Email Notifications**: Alert users of high spending
10. **Data Import**: Upload transactions from CSV

## Troubleshooting

### Issue: "Address already in use"
**Solution**: Flask is already running. Either:
- Close the previous Flask process
- Change port: `app.run(debug=True, port=5001)`

### Issue: Database "finance.db" not found
**Solution**: The database is created automatically on first run. If you delete it, restart the app to recreate it.

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution**: Install dependencies: `pip install -r requirements.txt`

### Issue: Transactions not saving
**Solution**: Check that:
- You're logged in (username shows in top right)
- All required fields are filled
- Amount is greater than 0
- Browser console shows no errors (F12)

## Performance Tips

- The app auto-refreshes data every 30 seconds
- For faster performance with large datasets, add database indexes
- Consider caching chart data for heavy users

## File Structure

- `app.py` (250+ lines): Main Flask application with all routes
- `templates/login.html` (40 lines): Login form
- `templates/register.html` (45 lines): Registration form
- `templates/index.html` (100+ lines): Dashboard with charts and transaction table
- `static/style.css` (400+ lines): Complete responsive styling
- `static/chart.js` (300+ lines): Charts, transaction management, and filtering

## Statistics

- **Total Lines of Code**: 1000+
- **Routes**: 8 main routes + 4 API endpoints
- **Features**: 12+ interactive features
- **Security**: 5+ security implementations
- **Responsive**: Mobile, tablet, and desktop optimized

## License

This project is open source and available for educational purposes.

## Author

Built with ❤️ as a demonstration of full-stack web development.

---

## Quick Start Summary

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
python app.py

# 3. Open browser
# Navigate to http://localhost:5000

# 4. Register and start tracking!
```

Enjoy tracking your finances! 💸
