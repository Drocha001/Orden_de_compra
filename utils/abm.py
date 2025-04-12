""" Voy a recoger por parametro si se trata de alta de articulos, clientes, proveedores, rubros, o sub rubros
 y a conectar con la base de datos mysql, la base local se deberia actualizar sola
 """

# hacer unica funcion para que ejecute ABM 
# utils

import mysql.connector
from conexion import MYSQL_CONFIG

def ejecutar_operacion(tabla, datos=None, operacion='alta', condiciones=None):
    """ Realiza una operación en la tabla especificada (alta, baja, modificación, búsqueda, depuración). """
    try:
        # Conexión a MySQL
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()

        if operacion == 'alta':
            if tabla == 'usuarios':
                if datos is None:
                    return "Datos no proporcionados para la operación de alta."
                # Preparar la consulta SQL para alta de usuarios
                query = """
                    INSERT INTO usuarios (nombre_usuario, clave, apellido, nombre, rol, activo)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                values = (
                    datos["nombre_usuario"],
                    datos["clave"],
                    datos["apellido"],
                    datos["nombre"],
                    datos["rol"],
                    datos.get("activo", True),  # Usar True como valor predeterminado
                )
                cursor.execute(query, values)
                conn.commit()
                return f"Alta en usuarios realizada con éxito. ID: {cursor.lastrowid}"
            else:
                if datos is None:
                    return "Datos no proporcionados para la operación de alta."
                # Preparar la consulta SQL para alta
                columnas = ', '.join(datos.keys())
                valores = ', '.join(['%s'] * len(datos))
                sql = f"INSERT INTO {tabla} ({columnas}) VALUES ({valores})"
                cursor.execute(sql, tuple(datos.values()))
                conn.commit()
                return f"Alta en {tabla} realizada con éxito. ID: {cursor.lastrowid}"

        elif operacion == 'baja':
            if condiciones is None:
                return "Condiciones no proporcionadas para la operación de baja."
            # Preparar la consulta SQL para baja
            sql = f"DELETE FROM {tabla} WHERE {condiciones}"
            cursor.execute(sql)
            conn.commit()
            return f"Baja en {tabla} realizada con éxito."

        elif operacion == 'modificacion':
            if datos is None or condiciones is None:
                return "Datos o condiciones no proporcionados para la operación de modificación."
            # Preparar la consulta SQL para modificación
            set_clause = ', '.join([f"{col} = %s" for col in datos.keys()])
            sql = f"UPDATE {tabla} SET {set_clause} WHERE {condiciones}"
            cursor.execute(sql, tuple(datos.values()))
            conn.commit()
            return f"Modificación en {tabla} realizada con éxito."

        elif operacion == 'busqueda':
            if condiciones is None:
                return "Condiciones no proporcionadas para la operación de búsqueda."
            # Preparar la consulta SQL para búsqueda
            sql = f"SELECT * FROM {tabla} WHERE {condiciones}"
            cursor.execute(sql)
            resultados = cursor.fetchall()
            return resultados

        elif operacion == 'depuracion':
            # Mostrar el estado del campo "activo" de la tabla "usuarios"
            if tabla == "usuarios":
                cursor.execute("SELECT id, nombre_usuario, activo FROM usuarios")
                resultados = cursor.fetchall()
                print("Estado del campo 'activo' en la tabla 'usuarios':")
                for resultado in resultados:
                    print(f"ID: {resultado[0]}, Usuario: {resultado[1]}, Activo: {resultado[2]}")
                return resultados
            else:
                return f"La operación de depuración no está disponible para la tabla {tabla}."

        else:
            return "Operación no válida."

    except mysql.connector.Error as e:
        return f"Error al realizar la operación en {tabla}: {e}"

    finally:
        cursor.close()
        conn.close()

# Ejemplos de uso:
# Alta
# nuevo_articulo = {"descripcion": "Laptop Gamer", "rubro": 1, "stock": 50.5}
# print(ejecutar_operacion("articulos", datos=nuevo_articulo, operacion='alta'))

# Baja
# print(ejecutar_operacion("articulos", operacion='baja', condiciones="id = 1"))

# Modificación
# CUIDADO DE NO PASAR EL ID DENTRO DEL DCCIONARIO YA QUE PROVOCA ERROR
# datos_modificados = {"descripcion": "Laptop Gamer Pro", "stock": 45.0}
# print(ejecutar_operacion("articulos", datos=datos_modificados, operacion='modificacion', condiciones="id = 1"))
# se puede indicar el diccionario directamnete si llega a ser necesario
#print(ejecutar_operacion("articulos",{"descripcion": "Laptop Gamer Pro", "stock": 45.0}, operacion='modificacion', condiciones="id = 4"))


# Búsqueda
# print(ejecutar_operacion("articulos", operacion='busqueda', condiciones="rubro = 1"))
