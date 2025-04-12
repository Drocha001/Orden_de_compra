import os
import sqlite3
import mysql.connector
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv()  # Cargar variables desde .env

MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "149.50.141.73"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "leonel5+"),
    "database": os.getenv("MYSQL_DATABASE", "sigma")
}


SQLITE_CONFIG = {
    
    "database":  os.path.join( "database", "local.db")
    
}

def get_mysql_connection():
    """Devuelve una conexión a MySQL."""
    return mysql.connector.connect(**MYSQL_CONFIG)

def get_sqlite_connection(db_name="local.db"):
    """Devuelve una conexión a una base de datos SQLite."""
    db_path = SQLITE_CONFIG.get(db_name)
    if not db_path:
        raise ValueError(f"Base de datos '{db_name}' no definida en SQLITE_CONFIG.")
    
    return sqlite3.connect(db_path)

