import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

CONFIG = {
    "driver": os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server"),
    "server": os.getenv("DB_SERVER"),
    "username": os.getenv("DB_USERNAME"),
    "password": os.getenv("DB_PASSWORD"),
}

def conectar_bd():
    """Establece conexión con SQL Server usando autenticación SQL (usuario y contraseña)."""
    try:
        conn = pyodbc.connect(
            f"DRIVER={{{CONFIG['driver']}}};"
            f"SERVER={CONFIG['server']};"
            f"UID={CONFIG['username']};"
            f"PWD={CONFIG['password']};"
            f"TrustServerCertificate=yes;",
            autocommit=True
        )
        return conn
    except pyodbc.Error as e:
        print("\033[31mError de conexión:\033[0m", e.args[1]) 
        return None

def probar_conexion():
    """Prueba la conexión a la base de datos."""
    conn = conectar_bd()
    if conn:
        print("\033[32mConexión a SQL Server exitosa.\033[0m")
        conn.close()
    else:
        print("\033[31mNo se pudo establecer conexión con la base de datos.\033[0m")
