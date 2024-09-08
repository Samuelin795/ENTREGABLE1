from flask import Flask, render_template, request, redirect, url_for, session
from db import get_db_connection

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Cambia esta clave por una clave secreta

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
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
            return redirect(url_for('amenu'))  # Redirige a '/amenu'
        else:
            return "Invalid credentials"
    return render_template('login.html')

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
            
            return redirect(url_for('amenu'))  # Redirige a '/amenu'
        
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

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/amenu', methods=['GET', 'POST'])
def amenu():
    if 'username' not in session:
        return redirect(url_for('home'))

    username = session['username']
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == 'POST':
        # Obtener las áreas de interés seleccionadas
        selected_areas = request.form.getlist('areas')

        # Guarda las áreas de interés en la base de datos (suponiendo que tienes una tabla user_areas)
        cursor.execute("DELETE FROM user_areas WHERE username = %s", (username,))
        for area in selected_areas:
            cursor.execute("INSERT INTO user_areas (username, area) VALUES (%s, %s)", (username, area))
        connection.commit()

        return redirect(url_for('view_products'))

    # Si es GET, mostrar el formulario con las posibles áreas de productos
    cursor.execute("SELECT DISTINCT area_name FROM areas")
    areas = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return render_template('amenu.html', areas=areas)

@app.route('/view_products')
def view_products():
    if 'username' not in session:
        return redirect(url_for('home'))

    username = session['username']
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Obtener las áreas seleccionadas por el usuario
    cursor.execute("SELECT area FROM user_areas WHERE username = %s", (username,))
    areas = cursor.fetchall()
    
    # Convertir a una lista de nombres de áreas
    selected_areas = [area['area'] for area in areas]

    # Obtener productos para las áreas seleccionadas
    if selected_areas:
        query = "SELECT name, price, image_url, area FROM products WHERE area IN (%s)" % ','.join(['%s'] * len(selected_areas))
        cursor.execute(query, selected_areas)
        products = cursor.fetchall()
    else:
        products = []

    cursor.close()
    connection.close()

    return render_template('view_products.html', products=products)

if __name__ == "__main__":
    app.run(debug=True)