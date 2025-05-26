import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",        # Cambia esto
        password="Juanjose/11", # Cambia esto
        database="super_uno",
        port=3310
    )
