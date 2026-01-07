from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd

# Configure Flask
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite
db = SQL("sqlite:///finance.db")

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.jinja_env.filters["usd"] = usd

# -----------------------
# ROUTES
# -----------------------

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    stocks = db.execute("""
        SELECT symbol, SUM(shares) as total_shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING total_shares > 0
    """, user_id)

    portfolio = []
    grand_total = 0
    for stock in stocks:
        quote = lookup(stock["symbol"])
        total_value = stock["total_shares"] * quote["price"]
        grand_total += total_value
        portfolio.append({
            "symbol": stock["symbol"],
            "shares": stock["total_shares"],
            "price": quote["price"]
        })

    cash_row = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = cash_row[0]["cash"]
    grand_total += cash

    return render_template("index.html", portfolio=portfolio, cash=cash, grand_total=grand_total)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username")
        if not password or not confirmation:
            return apology("must provide password")
        if password != confirmation:
            return apology("passwords do not match")

        hash_pw = generate_password_hash(password)

        try:
            new_user = db.execute(
                "INSERT INTO users (username, hash, cash) VALUES (?, ?, 10000)",
                username, hash_pw
            )
        except:
            return apology("username already exists")

        session["user_id"] = new_user
        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            return apology("must provide username and password")
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username or password")
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol")
        stock = lookup(symbol)
        if stock is None:
            return apology("invalid symbol")
        return render_template("quoted.html", stock=stock)
    else:
        return render_template("quote.html")

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        if not symbol:
            return apology("must provide symbol")
        stock = lookup(symbol)
        if stock is None:
            return apology("invalid symbol")
        try:
            shares = int(shares)
            if shares <= 0:
                raise ValueError
        except:
            return apology("invalid shares")

        user_id = session["user_id"]
        cash_row = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        cash = cash_row[0]["cash"]
        cost = shares * stock["price"]

        if cost > cash:
            return apology("cannot afford")

        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", cost, user_id)
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   user_id, stock["symbol"], shares, stock["price"])

        return redirect("/")

    else:
        return render_template("buy.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    user_id = session["user_id"]
    stocks = db.execute("""
        SELECT symbol, SUM(shares) as total_shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING total_shares > 0
    """, user_id)

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must select symbol")

        stock_owned = db.execute("""
            SELECT SUM(shares) as total
            FROM transactions
            WHERE user_id = ? AND symbol = ?
        """, user_id, symbol)

        total_owned = stock_owned[0]["total"]
        try:
            shares = int(shares)
            if shares <= 0 or shares > total_owned:
                raise ValueError
        except:
            return apology("invalid shares")

        stock = lookup(symbol)
        proceeds = shares * stock["price"]

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", proceeds, user_id)
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   user_id, symbol, -shares, stock["price"])
        return redirect("/")
    else:
        return render_template("sell.html", stocks=stocks)

@app.route("/history")
@login_required
def history():
    user_id = session["user_id"]
    transactions = db.execute("""
        SELECT symbol, shares, price, datetime(timestamp, 'localtime') as timestamp
        FROM transactions
        WHERE user_id = ?
        ORDER BY timestamp DESC
    """, user_id)

    # Add type
    for t in transactions:
        t["type"] = "BUY" if t["shares"] > 0 else "SELL"
        t["shares"] = abs(t["shares"])

    return render_template("history.html", transactions=transactions)
