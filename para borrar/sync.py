import sqlite3
import threading
import time
from conexion import MYSQL_CONFIG, SQLITE_CONFIG,  get_mysql_connection

import mysql.connector

# Intervalo de sincronización en segundos (900 seg = 15 minutos)
SYNC_INTERVAL = 10
sync_count = 0  # Contador de sincronizaciones

def create_local_database():
    """Crea la base de datos SQLite local si no existe."""
    conn = sqlite3.connect(SQLITE_CONFIG.get("database", "local.db"))
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS proveedores (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        cuit INTEGER NOT NULL,
        domicilio TEXT,
        
        localidad TEXT,
        provincia TEXT,
        empresa TEXT,
        telefono INTEGER,
        mail,TEXT,
        activo BOOLEAN
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS articulos (
        id INTEGER PRIMARY KEY,
        descripcion TEXT NOT NULL,
        rubro INTEGER,
        stock REAL
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS rubro (
        id INTEGER PRIMARY KEY,
        descripcion TEXT NOT NULL
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS subrubro (
        id INTEGER PRIMARY KEY,
        descripcion TEXT NOT NULL
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        dni  INTEGER NOT NULL,
        domicilio TEXT,            
        localidad TEXT,
        provincia TEXT,
        telefono INTEGER,
        mail,TEXT,
        activo BOOLEAN
    )''')
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
    #create_database_remota()

    print("Base de datos y tablas creadas exitosamente.")


"""def sync_with_mysql():
    #Sincroniza los datos de MySQL a SQLite periódicamente.
    global sync_count
    while True:
        sync_count += 1
        print(f"Iniciando sincronización # {sync_count} con MySQL...")
        mysql_conn = None
        sqlite_conn = None
        try:
            # Conexión a MySQL
            mysql_conn = mysql.connector.connect(**MYSQL_CONFIG)
            mysql_cursor = mysql_conn.cursor()

            # Conexión a SQLite
            sqlite_conn = sqlite3.connect(SQLITE_CONFIG.get("database", "local.db"))
            sqlite_cursor = sqlite_conn.cursor()

            tablas = ["proveedores", "articulos", "rubro", "subrubro", "pedidos"]
            
            for tabla in tablas:
                mysql_cursor.execute(f"SELECT * FROM {tabla}")
                registros = mysql_cursor.fetchall()

                sqlite_cursor.execute(f"DELETE FROM {tabla}")  # Borra datos anteriores
                
                for registro in registros:
                    placeholders = ','.join(['?'] * len(registro))
                    sqlite_cursor.execute(f"INSERT INTO {tabla} VALUES ({placeholders})", registro)

            sqlite_conn.commit()
            print(f"Sincronización #{sync_count} completada.")
        
        except Exception as e:
            print(f"Error en la sincronización #{sync_count}: {e}")
        
        finally:
            if sqlite_conn:
                sqlite_conn.close()
            if mysql_conn:
                mysql_conn.close()
        
        time.sleep(SYNC_INTERVAL)  # Esperar antes de la próxima sincronización"""

def sync_with_mysql():
    #############

    
    ###############
    """Sincroniza los datos de MySQL a SQLite periódicamente."""
    global sync_count
    while True:
        sync_count += 1
        print(f"Iniciando sincronización # {sync_count} con MySQL...")
        mysql_conn = None
        sqlite_conn = None
        try:
            # Conexión a MySQL
            mysql_conn = mysql.connector.connect(**MYSQL_CONFIG)
            mysql_cursor = mysql_conn.cursor()

            # Conexión a SQLite
            sqlite_conn = sqlite3.connect(SQLITE_CONFIG.get("database", "local.db"))
            sqlite_cursor = sqlite_conn.cursor()

            tablas = ["proveedores", "articulos", "rubro", "subrubro", "pedidos"]

            for tabla in tablas:
                mysql_cursor.execute(f"SELECT * FROM {tabla}")
                registros = mysql_cursor.fetchall()

                # Obtener nombres de columnas para la tabla
                columnas = [desc[0] for desc in mysql_cursor.description]
                placeholders = ','.join(['?'] * len(columnas))  # Ajustar número de parámetros

                sqlite_cursor.execute(f"DELETE FROM {tabla}")  # Borra datos anteriores
                
                for registro in registros:
                    registro = list(registro)  # Convertir tupla en lista para modificar datos
                    
                    # Convertir BOOLEAN de MySQL a INTEGER en SQLite
                    if tabla in ["proveedores", "clientes"]:
                        registro[-1] = int(registro[-1])  # Convertir último campo (activo) a 0 o 1
                    
                    # Manejar valores `None` correctamente
                    registro = [None if val is None else val for val in registro]

                    sqlite_cursor.execute(f"INSERT INTO {tabla} VALUES ({placeholders})", registro)

            sqlite_conn.commit()
            print(f"Sincronización #{sync_count} completada.")

        except Exception as e:
            print(f"Error en la sincronización #{sync_count}: {e}")

        finally:
            if sqlite_conn:
                sqlite_conn.close()
            if mysql_conn:
                mysql_conn.close()

        time.sleep(SYNC_INTERVAL)  # Esperar antes de la próxima sincronización


def start_sync_thread():
    """Inicia la sincronización en un hilo separado."""
    sync_thread = threading.Thread(target=sync_with_mysql, daemon=True)
    sync_thread.start()
    return sync_thread
