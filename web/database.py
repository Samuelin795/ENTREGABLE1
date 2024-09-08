import mysql.connector

def create_connection():
    return mysql.connector.connect(
        host='buozjrm4aihgms75kuk6-mysql.services.clever-cloud.com',
        user='uqmrrimvkufu81dw',
        password='52LqkmkhX24OhZGInVpL',
        database='buozjrm4aihgms75kuk6'
    )
