import sqlite3
import threading
import time
import mysql.connector 
from conexion import MYSQL_CONFIG, SQLITE_CONFIG

# Intervalo de sincronización en segundos (15 minutos por defecto)
SYNC_INTERVAL = 5 # 900 segundos = 15 minutos

# Crear base de datos SQLite local
def create_local_database():
    conn = sqlite3.connect(SQLITE_CONFIG["database"])
    #$conn = sqlite3.connect(SQLITE_CONFIG["database"])  # Cambia "local.db" por "database"

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

# Sincronización de datos desde MySQL hacia SQLite
"""def sync_with_mysql():
    import mysql.connector
    while True:
        print("Iniciando sincronización con MySQL...")
        a=a+1
        print(a)
        try:
            mysql_conn = mysql.connector.connect(**MYSQL_CONFIG)
            mysql_cursor = mysql_conn.cursor()
            
            sqlite_conn = sqlite3.connect(SQLITE_CONFIG["database"])
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

# Iniciar la sincronización en un hilo separado
def start_sync_thread():
    sync_thread = threading.Thread(target=sync_with_mysql, daemon=True)
    
    sync_thread.start()


if __name__ == "__main__":
    #create_local_database()
    start_sync_thread()
    print("Base de datos local creada y sincronización automática iniciada.")
    
"""



stop_event = threading.Event()  # Bandera para detener la sincronización

sync_count=0
def sync_with_mysql():
    #import mysql.connector
    global sync_count
    while not stop_event.is_set():  # Mientras no se solicite detener
        
        sync_count += 1  # Incrementar contador
        print(f"Iniciando sincronización #{sync_count} con MySQL...")
        try:
            mysql_conn = mysql.connector.connect(**MYSQL_CONFIG)
            mysql_cursor = mysql_conn.cursor()
            
            sqlite_conn = sqlite3.connect(SQLITE_CONFIG["database"])
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
        
        stop_event.wait(SYNC_INTERVAL)  # Espera el tiempo de sincronización o detención

# Iniciar la sincronización en un hilo separado
def start_sync_thread():
    global sync_thread
    sync_thread = threading.Thread(target=sync_with_mysql, daemon=True)
    sync_thread.start()

# Función para detener la sincronización
def stop_sync():
    stop_event.set()  # Activa la bandera para detener el hilo
    print("Sincronización detenida.")
