from flask import Flask, render_template, request, redirect
import sqlite3
import random

app = Flask(__name__)

# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('CREATE TABLE IF NOT EXISTS routes (id INTEGER PRIMARY KEY, name TEXT)')
    conn.close()

# ---------- HOME ----------
@app.route('/')
def home():
    conn = sqlite3.connect('database.db')
    routes = conn.execute('SELECT * FROM routes').fetchall()
    conn.close()
    
    predictions = {r[0]: random.randint(20,100) for r in routes}
    
    return render_template('index.html', routes=routes, predictions=predictions)

# ---------- ADMIN ----------
@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method == 'POST':
        name = request.form['name']
        
        conn = sqlite3.connect('database.db')
        conn.execute('INSERT INTO routes (name) VALUES (?)', (name,))
        conn.commit()
        conn.close()
        
        return redirect('/admin')
    
    conn = sqlite3.connect('database.db')
    routes = conn.execute('SELECT * FROM routes').fetchall()
    conn.close()
    
    return render_template('admin.html', routes=routes)

# ---------- BOOK PAGE ----------
@app.route('/book')
def book():
    ride = request.args.get('ride')
    return render_template('book.html', ride=ride)

# ---------- DASHBOARD ----------
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# ---------- BOOKINGS ----------
@app.route('/bookings')
def bookings():
    return render_template('bookings.html')

# ---------- LOGIN / SIGNUP ----------
@app.route('/login')
def login():
    return render_template('login.html')

# ---------- RUN ----------
if __name__ == '__main__':
    init_db()
    app.run(debug=True)