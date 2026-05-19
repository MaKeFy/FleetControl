import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            try:
                cls._instance = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='L7mps.24',
                    database='mantenimiento_maquinaria'
                )
            except Error as e:
                print(f"Error crítico de conexión: {e}")
        return cls._instance