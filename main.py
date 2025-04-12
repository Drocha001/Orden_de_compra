import sys
import os
import time
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
from kivy.core.window import Window

# Agregar el directorio que contiene abm.py al PYTHONPATH
# version 0.0.1
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
from utils.abm import ejecutar_operacion

from gestion import mostrar_rol_usuario, inicio, MenuApp, SessionManager  # Importar SessionManager
from login import LoginApp

from sync import create_local_database, start_sync_thread, create_database_remota

# usar async como alternativa
# hacer hilo de seguimiento
a = 0  # SOLO UTILZADA PARA HACER ALGUNAS VARIACIONES EN LAS PRUEBAS

class PruebaPantalla(MDBoxLayout):
    pass


class Main(MDApp):
    def build(self):
        # Configuración inicial del tema
        self.theme_cls.material_style = 'M3'
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style_switch_animation_duration = 0.8
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"

        # Cargar el archivo KV
        return Builder.load_file('pantallas.kv')

    """def cambiar_tema(self):
        # Cambiar entre tema claro y oscuro
        self.theme_cls.primary_palette = (
            "Orange" if self.theme_cls.primary_palette == "Red" else "Red"
        )
        self.theme_cls.theme_style = (
            "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        )"""

    """def actualizar_menu(self):
        # Limpiar el contenido del RecycleView antes de actualizar
        self.root.ids.menu_recycleview.data = []
        # Agregar los nuevos elementos al menú
        self.root.ids.menu_recycleview.data = [
            {"text": "Opción 1", "icon": "home"},
            {"text": "Opción 2", "icon": "settings"},
            {"text": "Opción 3", "icon": "information"},
        ]"""

    def regresar_menu(self):
        """
        Regresa al menú principal y limpia los contenedores dinámicos.
        """
        print("Regresando al menú principal...")

        # Vaciar los contenedores dinámicos
        root = self.root
        if root:
            rv = root.ids.get("menu_recycleview", None)
            if rv:
                rv.data = []  # Vaciar los datos del RecycleView
                rv.refresh_from_data()  # Forzar la actualización visual
                print("RecycleView vaciado desde submenú.")

        # Detener la aplicación actual
        self.stop()

        # Reiniciar la aplicación del menú principal
        kv_path = 'models'
        kv_file = 'menu.kv'
        MenuApp(kv_path, kv_file).run()


if __name__ == "__main__":
    create_database_remota()  # Crear base de datos remota si no existe
    create_local_database()  # Crear base de datos local si no existe

    # Iniciar la aplicación de login
    login_app = LoginApp()  # Instanciar la clase LoginApp
    login_app.run()  # Ejecutar la aplicación de inicio de sesión

    # Restaurar el tamaño por defecto de la ventana después de cerrar la pantalla de inicio de sesión
    Window.restore()

    # Obtener los datos de login después de que la aplicación de login se cierre
    valido = login_app.valido
    id_usuario = login_app.id_usuario
    mensaje = login_app.mensaje
    rol = login_app.rol

    if valido:
        print(f"Bienvenido {mensaje}! Rol: {rol}")
        print("Base de datos local creada y sincronización automática iniciada.")
        start_sync_thread()  #sincornizacion base de datos en segundo plano

        # Configurar la sesión del usuario
        SessionManager.set_session(id_usuario, rol)

        # Ejecución principal
        try:
            kv_path = 'models'  # Asegurarse de que la ruta de la carpeta models sea correcta
            kv_file = 'menu.kv'

            # Crear instancia de MenuApp y ejecutar la aplicación principal
            menu_app = MenuApp(kv_path, kv_file)
            menu_app.run()

        except KeyboardInterrupt:
            print("Finalizando aplicación...")
        finally:
            # Limpiar la sesión al finalizar
            SessionManager.clear_session()
    else:
        print(f"Error: {mensaje}")

