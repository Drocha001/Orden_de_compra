""" Voy a recoger por parametro si se trata de alta de articulos, clientes, proveedores, rubros, o sub rubros
 y a conectar con la base de datos mysql, la base local se deberia actualizar sola
 
 ejemplo 
 
 nuevo_articulo = {
    "id": None,  # Si es autoincremental, se puede omitir
    "descripcion": "Laptop Gamer",
    "rubro": 1,
    "stock": 50.5
}
print(Alta_Articulo(nuevo_articulo))
 """
 # hacer unica funcion para que ejecute ABM 
 # utils
 
import mysql.connector
from conexion import MYSQL_CONFIG

def ejecutar_alta(tabla, datos):
    """ Inserta un nuevo registro en la tabla especificada con los datos proporcionados. """
    try:
        # Conexión a MySQL
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()

        # Preparar la consulta SQL dinámicamente
        columnas = ', '.join(datos.keys())
        valores = ', '.join(['%s'] * len(datos))
        sql = f"INSERT INTO {tabla} ({columnas}) VALUES ({valores})"
        
        # Ejecutar la consulta
        cursor.execute(sql, tuple(datos.values()))
        conn.commit()

        return f"Alta en {tabla} realizada con éxito. ID: {cursor.lastrowid}"
    
    except mysql.connector.Error as e:
        return f"Error al realizar el alta en {tabla}: {e}"
    
    finally:
        cursor.close()
        conn.close()

def Alta_Rub(rub):
    """Alta en la tabla rubro"""
    return ejecutar_alta("rubro", rub)

def Alta_Subrub(srub):
    """Alta en la tabla subrubro"""
    return ejecutar_alta("subrubro", srub)

def Alta_Cliente(cl):
    """Alta en la tabla clientes"""
    return ejecutar_alta("clientes", cl)

def Alta_Articulo(art):
    """Alta en la tabla articulos"""
    return ejecutar_alta("articulos", art)

def Alta_Proveedor(prov):
    """Alta en la tabla proveedores"""
    return ejecutar_alta("proveedores", prov)

def Alta_pedido(pedido):
    """Alta en la tabla pedidos"""
    return ejecutar_alta("pedidos", pedido)
