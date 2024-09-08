import mysql.connector
from dotenv import load_dotenv
from urllib.parse import urlparse
import os

load_dotenv()

mysql_url = os.getenv('MYSQL_URL')
parsed_url = urlparse(mysql_url)

def get_db_connection():
    db_config = {
        'host': parsed_url.hostname,
        'port': parsed_url.port,
        'user': parsed_url.username,
        'password': parsed_url.password,
        'database': parsed_url.path[1:]
    }
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None
