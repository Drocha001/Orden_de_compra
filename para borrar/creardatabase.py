import sqlite3
import mysql.connector
import threading
import time
import cone

SYNC_INTERVAL = 900  # Intervalo de sincronización en segundos (15 minutos por defecto)

import mysql.connector

from conexion import get_mysql_connection

def create_database_remota():
    try:
        # Conectar a MySQL usando los datos de conexion.py
        conn = get_mysql_connection()
        cursor = conn.cursor()

        # Crear la base de datos si no existe
        cursor.execute("CREATE DATABASE IF NOT EXISTS sigma")
        cursor.execute("USE sigma")

        # Tabla Proveedores
        cursor.execute('''CREATE TABLE IF NOT EXISTS proveedores (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(150) NOT NULL,
            cuit BIGINT NOT NULL,
            domicilio VARCHAR(150),
            localidad VARCHAR(150),
            provincia VARCHAR(150),
            empresa VARCHAR(150),
            telefono BIGINT,
            activo BOOLEAN
        )''')

        # Tabla Artículos
        cursor.execute('''CREATE TABLE IF NOT EXISTS articulos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            descripcion VARCHAR(150) NOT NULL,
            rubro INT,
            stock DECIMAL(10,2)
        )''')

        # Tabla Rubro
        cursor.execute('''CREATE TABLE IF NOT EXISTS rubro (
            id INT AUTO_INCREMENT PRIMARY KEY,
            descripcion VARCHAR(150) NOT NULL
        )''')

        # Tabla Subrubro
        cursor.execute('''CREATE TABLE IF NOT EXISTS subrubro (
            id INT AUTO_INCREMENT PRIMARY KEY,
            descripcion VARCHAR(150) NOT NULL
        )''')

        # Tabla Pedidos
        cursor.execute('''CREATE TABLE IF NOT EXISTS pedidos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            proveedor INT,
            comprador INT,
            domicilio VARCHAR(250),
            viajante VARCHAR(250),
            iva VARCHAR(150),
            cuit BIGINT,
            vencimiento DATE,
            articulo INT,
            descripcion VARCHAR(250),
            cantidad INT,
            precio_unitario DECIMAL(10,2),
            total_art DECIMAL(10,2),
            plan_entrega DATE,
            percepcion_iva DECIMAL(10,2),
            subtotal1 DECIMAL(10,2),
            percepcion_ing_brutos DECIMAL(10,2),
            desrec DECIMAL(10,2),
            percepcion_ganancias DECIMAL(10,2),
            subtotal2 DECIMAL(10,2),
            percepcion_municipal DECIMAL(10,2),
            impuesto DECIMAL(10,2),
            otras_percepciones DECIMAL(10,2),
            total_pedido DECIMAL(10,2),
            observaciones TEXT,
            forma_pago VARCHAR(250),
            FOREIGN KEY (proveedor) REFERENCES proveedores(id),
            FOREIGN KEY (articulo) REFERENCES articulos(id)
        )''')

        # Confirmar cambios y cerrar conexión
        conn.commit()
        print("Base de datos y tablas creadas exitosamente.")

    except Exception as e:
        print(f"Error al crear la base de datos: {e}")

    finally:
        cursor.close()
        conn.close()

# Ejecutar la función
create_database_remota()

print("Base de datos y tablas creadas exitosamente.")

#


def create_database():
    conn = sqlite3.connect("local.db")
    cursor = conn.cursor()
    
    # Tabla Proveedores
    cursor.execute('''CREATE TABLE IF NOT EXISTS proveedores (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        cuit INTEGER NOT NULL,
        domicilio TEXT,
        localidad TEXT,
        provincia TEXT,
        empresa TEXT,
        telefono INTEGER,
        activo BOOLEAN
    )''')
    
    # Tabla Artículos
    cursor.execute('''CREATE TABLE IF NOT EXISTS articulos (
        id INTEGER PRIMARY KEY,
        descripcion TEXT NOT NULL,
        rubro INTEGER,
        stock REAL
    )''')
    
    # Tabla Rubro
    cursor.execute('''CREATE TABLE IF NOT EXISTS rubro (
        id INTEGER PRIMARY KEY,
        descripcion TEXT NOT NULL
    )''')
    
    # Tabla Subrubro
    cursor.execute('''CREATE TABLE IF NOT EXISTS subrubro (
        id INTEGER PRIMARY KEY,
        descripcion TEXT NOT NULL
    )''')
    
    # Tabla Pedidos
    cursor.execute('''CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY,
        proveedor INTEGER,
        comprador INTEGER,
        domicilio TEXT,
        viajante TEXT,
        iva TEXT,
        cuit INTEGER,
        vencimiento DATE,
        articulo INTEGER,
        descripcion TEXT,
        cantidad INTEGER,
        precio_unitario REAL,
        total_art REAL,
        plan_entrega DATE,
        percepcion_iva REAL,
        subtotal1 REAL,
        percepcion_ing_brutos REAL,
        desrec REAL,
        percepcion_ganancias REAL,
        subtotal2 REAL,
        percepcion_municipal REAL,
        impuesto REAL,
        otras_percepciones REAL,
        total_pedido REAL,
        observaciones TEXT,
        forma_pago TEXT
    )''')
    
    conn.commit()
    conn.close()

def sync_with_mysql():
    while True:
        print("Iniciando sincronización con MySQL...")
        #try:
        """mysql_conn = mysql.connector.connect(
                host="tu_host",
                user="tu_usuario",
                password="tu_contraseña",
                database="tu_base_datos"
            )"""
        try:
        # Conectar a MySQL usando los datos de conexion.py
            conn = get_mysql_connection()
            mysql_cursor = conn.cursor()
            #mysql_cursor = mysql_conn.cursor()
            
            sqlite_conn = sqlite3.connect("local.db")
            sqlite_cursor = sqlite_conn.cursor()
            
            tablas = ["proveedores", "articulos", "rubro", "subrubro", "pedidos"]
            
            for tabla in tablas:
                mysql_cursor.execute(f"SELECT * FROM {tabla}")
                registros = mysql_cursor.fetchall()
                
                sqlite_cursor.execute(f"DELETE FROM {tabla}")
                
                for registro in registros:
                    placeholders = ','.join(['?'] * len(registro))
                    sqlite_cursor.execute(f"INSERT INTO {tabla} VALUES ({placeholders})", registro)
            
            sqlite_conn.commit()
            print("Sincronización completada.")
        except Exception as e:
            print(f"Error en la sincronización: {e}")
        finally:
            sqlite_conn.close()
            mysql_conn.close()
        
        time.sleep(SYNC_INTERVAL)

def start_sync_thread():
    sync_thread = threading.Thread(target=sync_with_mysql, daemon=True)
    sync_thread.start()

if __name__ == "__main__":
    create_database()
    start_sync_thread()
    print("Base de datos local creada y sincronización automática iniciada.")
