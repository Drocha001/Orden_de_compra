import sys
from kivy.lang import Builder
import os
from kivy.core.window import Window
from utils.abm import ejecutar_operacion
from login import LoginApp
from kivymd.app import MDApp  # Asegurarse de usar MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.toolbar import MDTopAppBar  # Cambiar MDToolbar por MDTopAppBar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout  # Usar MDBoxLayout para consistencia con KivyMD
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget

# Ruta base para los archivos KV
KV_BASE_PATH = 'models'  # Definir la constante global

"""ID DE USUARIO, DEBE USARSE PARA GUARDAR EN LA BASE DE DATOS EL VENDEDOR, COMPRAODR, ETC, Y SE 
UTILIZARA ESTE ID COMO RESTRICCION PARA QUE UN USUARIO NO PUEDA VER LO QUE HIZO OTRO
utilizar como referencia responsivelyout.py como referencia para detectatr el tipo de dispositivo y cargar la pantalla correspondiente
debe gestionar todo una unica funcion hay que descartar detecion de sistema opertaivo
"""

def inicio(os_type):
    print(f" H O L A   {os_type}")

def mostrar_rol_usuario(id_usuario, rol, kv_path, kv_file):
    """
    Muestra la interfaz y gestiona las acciones según el rol del usuario.
    """
    Window.size = (600, 600)
    print(f"-----> El rol del usuario es: {rol}, ID del usuario: {id_usuario}")

    # Diccionario para mapear roles a funciones
    rol_funciones = {
        "Administrador": gestionar_todo,
        "Backend": gestionar_pedidos,
        "Frontend": gestionar_pedidos_propios,
        "Vendedor": gestionar_pedidos_ventas,
    }

    # Ejecutar la función correspondiente al rol
    funcion = rol_funciones.get(rol)
    if funcion:
        funcion(id_usuario)
        if rol == "Administrador":
            MenuApp(kv_path, kv_file).run()
    else:
        print("Rol no reconocido. No tiene permisos asignados.")

def gestionar_todo(id_usuario):
    print(f"Gestionando todo para el usuario con ID: {id_usuario}")

def gestionar_pedidos(id_usuario):
    print(f"Gestionando pedidos para el usuario con ID: {id_usuario}")

def gestionar_pedidos_propios(id_usuario):
    print(f"Gestionando pedidos propios para el usuario con ID: {id_usuario}")

def gestionar_pedidos_ventas(id_usuario):
    print(f"Gestionando pedidos de ventas para el usuario con ID: {id_usuario}")

class MenuApp(MDApp):  # Cambiar App por MDApp
    def __init__(self, kv_path, kv_file, **kwargs):
        super().__init__(**kwargs)
        self.kv_path = kv_path
        self.kv_file = kv_file

    def build(self):
        return Builder.load_file(os.path.join(self.kv_path, self.kv_file))

    def menu_opcion(self, opcion):
        print(f"Opción seleccionada: {opcion}")
        if opcion == 'usuarios':
            self.cargar_pantalla_usuarios()

    def cargar_pantalla_usuarios(self):
        kv_file = 'users.kv'
        self.stop()
        UserApp(KV_BASE_PATH, kv_file, self.kv_path, self.kv_file).run()

    def cerrar_sesion(self):
        """
        Método para cerrar sesión y volver a la pantalla de login.
        """
        print("Cerrando sesión...")
        self.stop()
        LoginApp().run()

    def gestion_usuarios(self):
        """
        Navega a la pantalla de gestión de usuarios.
        """
        kv_file = 'users.kv'
        self.stop()
        UserApp(KV_BASE_PATH, kv_file, self.kv_path, self.kv_file).run()

    def gestion_pedidos(self):
        """
        Navega a la pantalla de gestión de pedidos.
        """
        kv_file = 'pedidos.kv'
        self.stop()
        UserApp(KV_BASE_PATH, self.kv_path, self.kv_file).run()

    def gestion_proveedores(self):
        """
        Navega a la pantalla de gestión de proveedores.
        """
        kv_file = 'proveedores.kv'
        self.stop()
        UserApp(KV_BASE_PATH, self.kv_path, self.kv_file).run()

    def gestion_articulos(self):
        """
        Navega a la pantalla de gestión de artículos.
        """
        kv_file = 'articulos.kv'
        self.stop()
        UserApp(KV_BASE_PATH, self.kv_path, self.kv_file).run()

    def abrir_menu_lateral(self):
        """
        Método para manejar la apertura del menú lateral.
        """
        print("Menú lateral abierto.")

class AltaUsuarioContent(MDBoxLayout):  # Widget personalizado para el formulario
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 10
        self.padding = 10
        self.size_hint_y = None
        self.height = "400dp"

        self.add_widget(MDTextField(
            id="nombre_usuario",
            hint_text="Nombre de Usuario",
            required=True,
            size_hint_x=0.9,
            pos_hint={"center_x": 0.5},
        ))
        self.add_widget(MDTextField(
            id="clave",
            hint_text="Clave",
            password=True,
            required=True,
            size_hint_x=0.9,
            pos_hint={"center_x": 0.5},
        ))
        self.add_widget(MDTextField(
            id="apellido",
            hint_text="Apellido",
            size_hint_x=0.9,
            pos_hint={"center_x": 0.5},
        ))
        self.add_widget(MDTextField(
            id="nombre",
            hint_text="Nombre",
            size_hint_x=0.9,
            pos_hint={"center_x": 0.5},
        ))

        # Botón para desplegar el menú de roles
        self.rol_button = MDRaisedButton(
            text="Seleccionar Rol",
            size_hint_x=0.9,
            pos_hint={"center_x": 0.5},
            on_release=self.open_menu
        )
        self.add_widget(self.rol_button)

        # Crear el menú desplegable
        self.menu_items = [
            {"text": "Administrador", "viewclass": "OneLineListItem", "on_release": lambda x="Administrador": self.set_rol(x)},
            {"text": "Backend", "viewclass": "OneLineListItem", "on_release": lambda x="Backend": self.set_rol(x)},
            {"text": "Frontend", "viewclass": "OneLineListItem", "on_release": lambda x="Frontend": self.set_rol(x)},
            {"text": "Vendedor", "viewclass": "OneLineListItem", "on_release": lambda x="Vendedor": self.set_rol(x)},
        ]
        self.menu = MDDropdownMenu(
            caller=self.rol_button,
            items=self.menu_items,
            width_mult=4,
        )

    def open_menu(self, *args):
        self.menu.open()

    def set_rol(self, rol):
        self.rol_button.text = rol
        self.menu.dismiss()

class UserApp(MDApp):  # Cambiar App por MDApp
    def __init__(self, kv_path, kv_file, menu_kv_path, menu_kv_file, **kwargs):
        super().__init__(**kwargs)
        self.kv_path = kv_path
        self.kv_file = kv_file
        self.menu_kv_path = menu_kv_path
        self.menu_kv_file = menu_kv_file

    def build(self):
        return Builder.load_file(os.path.join(self.kv_path, self.kv_file))

    def alta_usuario(self):
        """
        Muestra un formulario para el alta de un nuevo usuario.
        """
        self.dialog = MDDialog(
            title="Alta de Usuario",
            type="custom",
            content_cls=AltaUsuarioContent(),  # Usar el widget personalizado
            buttons=[
                MDRaisedButton(
                    text="CANCELAR",
                    on_release=lambda _: self.dialog.dismiss(),
                ),
                MDRaisedButton(
                    text="GUARDAR",
                    on_release=lambda _: self.guardar_usuario(),
                ),
            ],
        )
        self.dialog.open()

    def guardar_usuario(self):
        """
        Guarda el nuevo usuario en la base de datos.
        """
        content = self.dialog.content_cls
        data = {
            "nombre_usuario": content.children[3].text,
            "clave": content.children[2].text,
            "apellido": content.children[1].text,
            "nombre": content.children[0].text,
            "rol": content.rol_button.text,  # Obtener el texto del botón de rol
        }

        if not data["nombre_usuario"] or not data["clave"]:
            print("Error: Nombre de usuario y clave son obligatorios.")
            return

        try:
            ejecutar_operacion("usuarios", datos=data, operacion="alta")
            print(f"Usuario {data['nombre_usuario']} creado exitosamente.")
        except Exception as e:
            print(f"Error al crear el usuario: {e}")
        finally:
            self.dialog.dismiss()

    def baja_usuario(self):
        ejecutar_operacion('baja')

    def modificacion_usuario(self):
        ejecutar_operacion('modificacion')

    def consulta_usuarios(self):
        """
        Consulta y muestra el listado de usuarios.
        """
        try:
            usuarios = ejecutar_operacion("usuarios", operacion="busqueda", condiciones="activo = 1")
            usuarios_list = self.root.ids.usuarios_list  # Asegurarse de que el ID esté definido
            usuarios_list.clear_widgets()

            for usuario in usuarios:
                item = OneLineIconListItem(
                    text=f"{usuario[3]} {usuario[2]} - {usuario[4]}"
                )
                item.add_widget(IconLeftWidget(icon="account"))
                usuarios_list.add_widget(item)
        except Exception as e:
            print(f"Error al consultar usuarios: {e}")

    def regresar_menu(self):
        self.stop()
        MenuApp(self.menu_kv_path, self.menu_kv_file).run()

    def alta_articulo(self):
        print("Alta de Artículo")
        # Lógica para alta de artículo

    def consulta_articulos(self):
        print("Consulta de Artículos")
        # Lógica para consulta de artículos

    def modificacion_articulo(self):
        print("Modificación de Artículo")
        # Lógica para modificación de artículo

    def baja_articulo(self):
        print("Baja de Artículo")
        # Lógica para baja de artículo

if __name__ == "__main__":
    if len(sys.argv) > 2:
        id_usuario = sys.argv[1]
        rol_usuario = sys.argv[2]
        kv_path = KV_BASE_PATH
        kv_file = 'menu.kv'
        mostrar_rol_usuario(id_usuario, rol_usuario, kv_path, kv_file)
    else:
        print("No se ha proporcionado el ID y el rol del usuario.")