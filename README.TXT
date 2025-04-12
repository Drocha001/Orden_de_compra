
// proyecyo sigma+ "Sistema Integral de Gestión  Mantenimiento ( puede ser mercadeo) y Administración"

AVANCES:
* INTERFACES GRAFICAS BASICAS
* LOGIN DESDE BASE DE DATOS, FEIFICACION DE USUARIO ACTIVO O INEXISTENTE
* GESTION DE USUARIOS
* FUNCIONA LA SINCORNIZACION ENTRE UNA BASE DE DATOS REOMTAS Y UNA BASE LOCAL 
* SE UBICO BASE DE DATOS LOCALE EN CARPETA /DATABEASE
* SE OPTIMIZO FUNCION ejecutar_operacion(tabla, datos=None, operacion='alta', condiciones=None): PARA QUEDE LA MISMA FUNCION SE REALICEN
  ABM, SOLO PASANDO NOMBRE DE LA TABLA, LOS DATOS EN FORMAT DICIONARIO, LA OPERACION Y LAS CONDICIONES POR PARAMETRO.
* SE UBICO ABM EN CARPETA /UTILS


PENDIENTES: 
HACER AMB DESDE BASES DE DATOS COMENZAR CON BACKEND
HACER LOGIN Y DAR ACESESO SEGUN PERFIL
PRERARA LA APLICAIN PARA DETECTAR TIPO DE PANTALLA, Y/O SISTEMA OPERATIVO, VOLTEAR PANTALLA RESPOSIVE
HACER LOS MENUS




DATOSDE CONECCION
Comando	Descripción
mysql -h <host> -u <usuario> -p	Conectarse a MySQL
USE <base_de_datos>;	Seleccionar una base de datos
SHOW TABLES;	Listar las tablas
SELECT * FROM <tabla>;	Ver los datos de una tabla
DESC <tabla>;	Ver la estructura de una tabla
EXIT;	Salir de MySQL

CADENA DE CONEXION EN SH
mysql -h 149.50.141.73 -u root -p

USE sigma;

SHOW TABLES;

SELECT * FROM proveedores;

SELECT * FROM proveedores LIMIT 10;

DESC pedidos;

SHOW COLUMNS FROM pedidos;

DROP DATABASE sigma;  elimina base de datos

SHOW DATABASES;






📌 Tabla Resumen de Comandos SQL
Acción	Comando SQL
Eliminar una base de datos	DROP DATABASE nombre_de_tu_bd;
Ver bases de datos disponibles	SHOW DATABASES;
Seleccionar una base de datos	USE nombre_de_tu_bd;
Eliminar una tabla	DROP TABLE nombre_de_la_tabla;
Ver tablas en una base de datos	SHOW TABLES;
Ver estructura de una tabla	DESC nombre_de_la_tabla;
Agregar una nueva columna	ALTER TABLE nombre_de_la_tabla ADD COLUMN nombre_columna TIPO;
Modificar una columna existente	ALTER TABLE nombre_de_la_tabla MODIFY COLUMN nombre_columna NUEVO_TIPO;
Renombrar una columna	ALTER TABLE nombre_de_la_tabla CHANGE COLUMN nombre_actual nuevo_nombre TIPO;
Eliminar una columna	ALTER TABLE nombre_de_la_tabla DROP COLUMN nombre_columna;
Renombrar una tabla	ALTER TABLE nombre_actual RENAME TO nuevo_nombre;
Agregar clave foránea	ALTER TABLE pedidos ADD CONSTRAINT fk_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios(id);
Eliminar clave foránea	ALTER TABLE pedidos DROP FOREIGN KEY nombre_de_la_fk;
Modificar clave foránea con ON DELETE CASCADE	ALTER TABLE pedidos ADD CONSTRAINT fk_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE;
Verificar si un valor existe en una tabla	SELECT * FROM proveedores WHERE id = valor_que_estás_usando;
Insertar un nuevo registro	INSERT INTO nombre_de_la_tabla (columna1, columna2) VALUES (valor1, valor2);
Actualizar un registro	UPDATE nombre_de_la_tabla SET columna1 = nuevo_valor WHERE condicion;
Eliminar un registro	DELETE FROM nombre_de_la_tabla WHERE condicion;