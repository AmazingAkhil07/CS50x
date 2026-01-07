from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_change_this'

DATABASE = 'finance.db'

# Helper function to connect to database
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database
def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        
        c.execute('''CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )''')
        
        c.execute('''CREATE TABLE transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT,
            date TEXT NOT NULL,
            notes TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )''')
        
        conn.commit()
        conn.close()
        print("Database initialized!")

# Initialize database on startup
init_db()

# Routes

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/login')
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    conn.close()
    
    return render_template('index.html', username=user['username'])

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if not username or not password:
            return render_template('register.html', error='Username and password required!')
        
        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match!')
        
        if len(password) < 6:
            return render_template('register.html', error='Password must be at least 6 characters!')
        
        conn = get_db_connection()
        error = None
        
        try:
            conn.execute(
                'INSERT INTO users (username, password_hash) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            conn.commit()
        except sqlite3.IntegrityError:
            error = 'Username already exists!'
        finally:
            conn.close()
        
        if error:
            return render_template('register.html', error=error)
        
        return redirect('/login?success=registered')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            return redirect('/')
        
        return render_template('login.html', error='Invalid username or password!')
    
    success = request.args.get('success')
    return render_template('login.html', success=success)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# API Routes for transactions

@app.route('/api/add-transaction', methods=['POST'])
def add_transaction():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.json
    trans_type = data.get('type')
    amount = data.get('amount')
    category = data.get('category')
    date = data.get('date')
    notes = data.get('notes', '')
    
    if not all([trans_type, amount, category, date]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        amount = float(amount)
        if amount <= 0:
            return jsonify({'error': 'Amount must be greater than 0'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid amount'}), 400
    
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO transactions (user_id, type, amount, category, date, notes) VALUES (?, ?, ?, ?, ?, ?)',
        (session['user_id'], trans_type, amount, category, date, notes)
    )
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/api/get-transactions')
def get_transactions():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    conn = get_db_connection()
    transactions = conn.execute(
        'SELECT * FROM transactions WHERE user_id = ? ORDER BY date DESC',
        (session['user_id'],)
    ).fetchall()
    conn.close()
    
    return jsonify([dict(t) for t in transactions])

@app.route('/api/get-balance')
def get_balance():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    conn = get_db_connection()
    result = conn.execute(
        '''SELECT 
            COALESCE(SUM(CASE WHEN type='income' THEN amount ELSE 0 END), 0) as total_income,
            COALESCE(SUM(CASE WHEN type='expense' THEN amount ELSE 0 END), 0) as total_expense
        FROM transactions WHERE user_id = ?''',
        (session['user_id'],)
    ).fetchone()
    conn.close()
    
    total_income = result['total_income']
    total_expense = result['total_expense']
    balance = total_income - total_expense
    
    return jsonify({
        'balance': balance,
        'income': total_income,
        'expense': total_expense
    })

@app.route('/api/get-chart-data')
def get_chart_data():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    conn = get_db_connection()
    
    # Expense by category
    expenses = conn.execute(
        '''SELECT category, SUM(amount) as total 
        FROM transactions WHERE user_id = ? AND type='expense' 
        GROUP BY category''',
        (session['user_id'],)
    ).fetchall()
    
    # Balance over time
    daily_balance = conn.execute(
        '''SELECT date, 
            SUM(CASE WHEN type='income' THEN amount ELSE -amount END) as daily_change
        FROM transactions WHERE user_id = ? 
        GROUP BY date ORDER BY date''',
        (session['user_id'],)
    ).fetchall()
    
    conn.close()
    
    # Calculate cumulative balance
    cumulative = 0
    balance_over_time = []
    for row in daily_balance:
        cumulative += row['daily_change']
        balance_over_time.append({'date': row['date'], 'balance': cumulative})
    
    return jsonify({
        'expenses_by_category': [{'category': e['category'], 'amount': e['total']} for e in expenses],
        'balance_over_time': balance_over_time
    })

@app.route('/api/delete-transaction/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    conn = get_db_connection()
    # Verify transaction belongs to user
    trans = conn.execute(
        'SELECT user_id FROM transactions WHERE id = ?',
        (transaction_id,)
    ).fetchone()
    
    if not trans or trans['user_id'] != session['user_id']:
        conn.close()
        return jsonify({'error': 'Unauthorized'}), 403
    
    conn.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
