from flask import Flask, render_template, request, redirect, url_for, session
from db import get_db_connection

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Cambia esta clave por una clave secreta

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('welcome'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.form['username']
        password = request.form['password']
        
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        if user:
            session['username'] = user['username']
            return redirect(url_for('welcome'))
        else:
            return "Invalid credentials"
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            
            connection = get_db_connection()
            cursor = connection.cursor()
            
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                cursor.close()
                connection.close()
                return "Username already exists"
    
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            connection.commit()
            
            cursor.close()
            connection.close()
            
            return redirect(url_for('home'))
        
        return render_template('register.html')
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/welcome')
def welcome():
    if 'username' not in session:
        return redirect(url_for('home'))
    return f"Welcome, {session['username']}!"

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.errorhandler(Exception)
def handle_exception(e):
    # Puedes agregar lógica para registrar el error o mostrar una página de error personalizada
    return f"An unexpected error occurred: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)
