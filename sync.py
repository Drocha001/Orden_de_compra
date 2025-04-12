import sqlite3
import threading
import time
from conexion import MYSQL_CONFIG, SQLITE_CONFIG, get_mysql_connection
import mysql.connector
from decimal import Decimal

"""                         IMPORTANTE, AL MODIFICAR UNA BASE DE DATOS, MYSQL, HAY QUE MODIFICAR TAMBIEN 
                            SQLITE3 Y PRESTAR ATENCION AL LOS FORMATOS DE LOS CAMPOS Y VICEVERSA
"""

SYNC_INTERVAL = 3600      #900  15 minutos # Intervalo de sincronización en segundos (1 hora)
sync_count = 0 #cuenta clas veces que se va sincronizando, para uso de depuracion

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
            mail TEXT,
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
        
        #tabla clientes
        cursor.execute("""CREATE TABLE IF NOT EXISTS clientes (
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       nombre TEXT NOT NULL,
                       dni  INTEGER NOT NULL,utils
                       domicilio TEXT,
                       localidad TEXT,
                       provincia TEXT,
                       telefono INTEGER,
                       mail TEXT,
                       activo BOOLEAN
                    )""")
        # Tabla Usuarios
        cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre_usuario VARCHAR(150) NOT NULL,
            clave VARCHAR(150) NOT NULL,
            apellido VARCHAR(150),
            nombre VARCHAR(150),
            rol VARCHAR(150),
            activo BOOLEAN
        )''')

        # Confirmar cambios y cerrar conexión
        conn.commit()
        print("Base de datos y tablas creadas exitosamente.")

    except Exception as e:
        print(f"Error al crear la base de datos: {e}")

    finally:
        cursor.close()
        conn.close()



    print("Base de datos y tablas creadas exitosamente.")

def create_local_database():
    """Crea la base de datos SQLite local si no existe."""
    conn = sqlite3.connect(SQLITE_CONFIG.get("database", "local.db"))
    #conn = sqlite3.connect(SQLITE_CONFIG.get)
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
        mail TEXT,
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
        mail TEXT,
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
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        nombre_usuario TEXT NOT NULL,
        clave TEXT NOT NULL,
        apellido TEXT,
        nombre TEXT,
        rol TEXT,
        activo BOOLEAN
    )''')
    
    conn.commit()
    conn.close()


def sync_with_mysql():  #funcion para sincronizar las bases de datos 
    global sync_count
    while True:
        sync_count += 1
        print(f"Iniciando sincronización # {sync_count} con MySQL...")
        mysql_conn = None
        sqlite_conn = None
        try:
            mysql_conn = mysql.connector.connect(**MYSQL_CONFIG)
            mysql_cursor = mysql_conn.cursor()
            sqlite_conn = sqlite3.connect(SQLITE_CONFIG.get("database", "local.db"))
            sqlite_cursor = sqlite_conn.cursor()

            tablas =["proveedores" ,"articulos", "rubro", "subrubro","clientes", "pedidos"]
            
            for tabla in tablas:
                mysql_cursor.execute(f"SELECT * FROM {tabla}")
                registros = mysql_cursor.fetchall()
                sqlite_cursor.execute(f"DELETE FROM {tabla}")
                
                for registro in registros:
                    registro = [float(x) if isinstance(x, Decimal) else x for x in registro]  # Convertir Decimal a float ya que los campos son diferentes en mysql y sqlite3
                    placeholders = ','.join(['?'] * len(registro))
                    try:
                        sqlite_cursor.execute(f"INSERT INTO {tabla} VALUES ({placeholders})", registro)
                    except Exception as e:
                        print(f"Error al insertar en {tabla}: {registro} -> {e}")

            sqlite_conn.commit()
            print(f"Sincronización #{sync_count} completada.") # muestra la cantidad de veces que se va sincroninando desde que esta en ejecucion
        
        except Exception as e:
            print(f"Error en la sincronización #{sync_count}: {e}")
        
        finally:
            if sqlite_conn:
                sqlite_conn.close()
            if mysql_conn:
                mysql_conn.close()
        
        time.sleep(SYNC_INTERVAL)

def start_sync_thread(): # inicia el hilo de sincornizacion en segundo plano
    sync_thread = threading.Thread(target=sync_with_mysql, daemon=True)
    sync_thread.start()
    return sync_thread
