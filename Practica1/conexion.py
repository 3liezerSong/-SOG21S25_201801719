import pyodbc

CONFIG = {
    "driver": "ODBC Driver 17 for SQL Server",
    "server": "DESKTOP\\MSSQLSERVER01", 
    "database": "master",
}


def conectar_bd():
    """Establece conexión con SQL Server usando autenticación de Windows."""
    try:
        conn = pyodbc.connect(
            f"DRIVER={CONFIG['driver']};"
            f"SERVER={CONFIG['server']};"
            f"DATABASE={CONFIG['database']};"
            "Trusted_Connection=yes;",  # Autenticación de Windows
            autocommit=True
        )
        return conn
    except pyodbc.Error as e:
        print("\033[31mError al conectar con la base de datos:\033[0m", e)
        return None

def probar_conexion():
    """Prueba la conexión a la base de datos."""
    conn = conectar_bd()
    if conn:
        print("\033[32mConexión a SQL Server exitosa.\033[0m")
        conn.close()
    else:
        print("\033[31mNo se pudo establecer conexión con la base de datos.\033[0m")
