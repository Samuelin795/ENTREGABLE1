import mysql.connector

# Parámetros de conexión
conn = mysql.connector.connect(
    host='your_host',
    user='your_user',
    password='your_password',
    database='your_database'
)

# Crear un cursor para ejecutar consultas
cursor = conn.cursor()

# Ejecutar una consulta
cursor.execute("SELECT * FROM your_table")

# Imprimir resultados
for row in cursor.fetchall():
    print(row)

# Cerrar la conexión
conn.close()
