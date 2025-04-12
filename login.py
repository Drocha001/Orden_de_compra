import os
from kivymd.app import MDApp  # Cambiar App por MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.core.window import Window
import sys
import platform  # Importar el módulo platform
import mysql.connector
from conexion import get_mysql_connection

class LoginApp(MDApp):  # Cambiar App por MDApp
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.valido = False
        self.id_usuario = None
        self.mensaje = ""
        self.rol = ""

    def build(self):
        # Configurar el tamaño inicial de la ventana
        #Window.size = (250, 200)  # Tamaño inicial de 5x10 cm aproximadamente
        return Builder.load_file('models/login.kv')  # Corregir la ruta del archivo KV

    def login(self, username, password):
        """
        Maneja el proceso de inicio de sesión.
        """
        self.valido, self.id_usuario, self.mensaje, self.rol = self.verificar_usuario(username, password)
        if self.valido:
            print(f"Bienvenido {self.mensaje}! Rol: {self.rol}")
            Window.restore()  # Restaurar el tamaño por defecto de la ventana
            self.stop()  # Cerrar la ventana de login
        else:
            # Mostrar mensaje de error en la ventana de login
            self.root.ids.error_message.text = self.mensaje
            # Vaciar los campos de usuario y contraseña
            self.root.ids.username.text = ""
            self.root.ids.password.text = ""

    def verificar_usuario(self, nombre_usuario, clave):
        """
        Verifica si el usuario existe y está activo.
        """
        try:
            conn = get_mysql_connection()
            cursor = conn.cursor()

            # Verificar si el usuario existe
            cursor.execute("SELECT id, nombre, apellido, rol, activo FROM usuarios WHERE nombre_usuario = %s", (nombre_usuario,))
            usuario = cursor.fetchone()

            if not usuario:
                return False, None, "El usuario no existe.", ""

            # Verificar si el usuario está activo
            if not usuario[4]:  # El campo 'activo' está en la posición 4
                return False, None, "El usuario no está activo.", ""

            # Verificar la contraseña
            cursor.execute("SELECT id, nombre, apellido, rol FROM usuarios WHERE nombre_usuario = %s AND clave = %s", (nombre_usuario, clave))
            usuario_valido = cursor.fetchone()

            if usuario_valido:
                return True, usuario_valido[0], usuario_valido[1], usuario_valido[3]  # Retorna True, id, nombre y rol
            else:
                return False, None, "Contraseña incorrecta.", ""

        except mysql.connector.Error as err:
            return False, None, "Error en la conexión a la base de datos.", str(err)

        finally:
            conn.close()

    def salir(self):
        print("Saliendo de la aplicación...")
        self.stop()
        sys.exit()

def get_os():
    os_name = platform.system()
    if os_name == "Linux":
        if "ANDROID_ARGUMENT" in os.environ:
            return "Android"
        else:
            return "Linux"
    elif os_name == "Windows":
        return "Windows"
    elif os_name == "Darwin":
        if "IOS_ARGUMENT" in os.environ:
            return "iOS"
        else:
            return "macOS"
    else:
        return "Unknown"

#parece que eesto no se ejecuta 
"""if __name__ == "__main__":
    os_type = get_os()
    print(f"aplicacion en : Ejecutando en: {os_type}")  # averigua que sistema operativo esta corriendo
    LoginApp(os_type).run()"""