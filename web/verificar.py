import mysql.connector
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

# Cargar las variables de entorno del archivo .env
load_dotenv()

# Obtener la URL de conexión desde las variables de entorno
mysql_url = os.getenv('MYSQL_URL')

# Imprimir la URL para depuración
print("MySQL URL:", mysql_url)

if mysql_url is None:
    raise ValueError("La variable de entorno MYSQL_URL no está configurada.")

# Desglosar la URL de conexión
parsed_url = urlparse(mysql_url)
host = parsed_url.hostname
port = parsed_url.port
user = parsed_url.username
password = parsed_url.password
database = parsed_url.path[1:]  # quitar el primer carácter '/' del nombre de la base de datos

# Imprimir valores para depuración
print("Host:", host)
print("Port:", port)
print("User:", user)
print("Password:", password)
print("Database:", database)

if port is None:
    raise ValueError("El puerto no está configurado correctamente en la URL.")

try:
    # Establecer conexión a la base de datos
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port
    )

    cursor = connection.cursor()
    cursor.execute("SELECT DATABASE();")
    result = cursor.fetchone()
    print("Connected to:", result)

    # Ejemplo de una consulta adicional
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    print("Tables in database:")
    for table in tables:
        print(table[0])

except mysql.connector.Error as err:
    print("Error:", err)

finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("Connection closed.")
