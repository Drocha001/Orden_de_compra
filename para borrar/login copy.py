import mysql.connector
from conexion import get_mysql_connection
""" 
+----+----------------+-------+----------+--------+---------------+-------------+--------+
| id | nombre_usuario | clave | apellido | nombre | rol           | privilegios | activo |
+----+----------------+-------+----------+--------+---------------+-------------+--------+
|  1 | Admin          | 3112  | Rocha    | Diego  | Administrador | NULL        |      1 |
|  2 | Back           | 3112  | Rocha    | Diego  | Backend       | NULL        |      1 |
|  3 | Front          | 3112  | Rocha    | Diego  | Frontend      | NULL        |      1 |
+----+----------------+-------+----------+--------+---------------+-------------+--------+

"""
def verificar_usuario(nombre_usuario, clave):
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, nombre, apellido, rol FROM usuarios WHERE nombre_usuario = %s AND clave = %s AND activo = 1", (nombre_usuario, clave))
        usuario = cursor.fetchone()
        
        conn.close()
        
        if usuario:
            return True, usuario[0], usuario[1], usuario[3]  # Retorna True, id, nombre y rol
        else:
            return False, "Usuario o clave incorrectos.", "Error"
    except mysql.connector.Error as err:
        return False, "Error", str(err)

def login():
    nombre_usuario = input("Ingrese su nombre de usuario: ")
    clave = input("Ingrese su clave: ")
    
    valido, id_usuario, mensaje, rol = verificar_usuario(nombre_usuario, clave)
    
    if valido:
        print(f"Bienvenido {mensaje}!")
        return True, id_usuario, mensaje, rol
    else:
        print(mensaje)
        return False, mensaje, rol