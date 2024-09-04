from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from dotenv import load_dotenv
from urllib.parse import urlparse
import os

# Cargar las variables de entorno del archivo .env
load_dotenv(dotenv_path='C:/Users/ESTUDIANTE/Desktop/ENTREGABLE1/web/.env')

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Cambia esta clave por una clave secreta

# Obtener la URL de conexión desde las variables de entorno
mysql_url = os.getenv('MYSQL_URL')

# Desglosar la URL de conexión
parsed_url = urlparse(mysql_url)
db_config = {
    'host': parsed_url.hostname,
    'port': parsed_url.port,
    'user': parsed_url.username,
    'password': parsed_url.password,
    'database': parsed_url.path[1:]  # quitar el primer carácter '/' del nombre de la base de datos
}

def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('welcome'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Comprobar si el nombre de usuario ya existe
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            cursor.close()
            connection.close()
            return "Username already exists"

        # Insertar el nuevo usuario
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        connection.commit()
        
        cursor.close()
        connection.close()
        
        return redirect(url_for('home'))
    
    return render_template('register.html')

@app.route('/welcome')
def welcome():
    if 'username' not in session:
        return redirect(url_for('home'))
    return f"Welcome, {session['username']}!"

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
