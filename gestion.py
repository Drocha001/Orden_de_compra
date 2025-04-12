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
from kivymd.uix.list import MDList, OneLineListItem  # Importar MDList y OneLineListItem
from kivymd.uix.selectioncontrol import MDCheckbox  # Importar MDCheckbox
from kivymd.uix.label import MDLabel  # Importar MDLabel
from kivy.factory import Factory
from kivy.properties import StringProperty
from utils.opcion_en_desarrollo import mostrar_opcion_en_desarrollo

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
            app = MenuApp(kv_path, kv_file)
            app.set_user_role(rol)
            app.run()
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

class CustomOneLineIconListItem(OneLineIconListItem):
    icon = StringProperty()  # Definir 'icon' como una propiedad de Kivy
#----------
    def reset(self):
        """
        Restablece las propiedades del elemento a valores predeterminados.
        """
        self.text = ""  # Vaciar el texto
        self.icon = ""  # Vaciar el icono
        self.on_press = None  # Eliminar cualquier acción asociada
#------------------------
class SessionManager:
    """
    Clase para gestionar el estado de la sesión.
    """
    user_role = None  # Rol del usuario
    user_id = None  # ID del usuario

    @classmethod
    def set_session(cls, user_id, user_role):
        cls.user_id = user_id
        cls.user_role = user_role

    @classmethod
    def clear_session(cls):
        cls.user_id = None
        cls.user_role = None

# Modifica la clase MenuApp para usar el rol del usuario desde SessionManager
class MenuApp(MDApp):  # Cambiar App por MDApp
    def __init__(self, kv_path, kv_file, **kwargs):
        super().__init__(**kwargs)
        self.kv_path = kv_path
        self.kv_file = kv_file
        self.user_role = None  # Variable para almacenar el rol del usuario
        self.menu_initialized = False  # Bandera para controlar la inicialización del menú

    def set_user_role(self, role):
        """
        Establece el rol del usuario.
        """
        self.user_role = role

    def build(self):
        root = Builder.load_file(os.path.join(self.kv_path, self.kv_file))

        # Obtener el rol del usuario desde SessionManager
        self.user_role = SessionManager.user_role
        if not self.user_role:
            print("Error: El rol del usuario no está configurado en la sesión.")
            return root

        # Limpiar los datos existentes en el RecycleView
        rv = root.ids.menu_recycleview
        print(f"Antes de limpiar: {len(rv.data)} elementos en rv.data")  # Depuración
        rv.data = []  # Vaciar los datos del RecycleView
        rv.refresh_from_data()  # Forzar la actualización visual
        print(f"Después de limpiar: {len(rv.data)} elementos en rv.data")  # Depuración

        # Generar dinámicamente las opciones del menú si no se ha inicializado
        if not self.menu_initialized:
            self.menu_initialized = True  # Marcar como inicializado
            menu_items = [
                {"text": "Gestión de Usuarios", "icon": "account-group", "on_press": self.gestion_usuarios, "roles": ["Administrador"]},
                {"text": "Gestión de Pedidos", "icon": "clipboard-list", "on_press": self.gestion_pedidos, "roles": ["Administrador", "Backend", "Frontend", "Vendedor"]},
                {"text": "Gestión de Proveedores", "icon": "truck", "on_press": self.gestion_proveedores, "roles": ["Administrador", "Backend", "Frontend"]},
                {"text": "Gestión de Artículos", "icon": "package-variant", "on_press": self.gestion_articulos, "roles": ["Administrador", "Backend", "Frontend", "Vendedor"]},
                {"text": "Cerrar Sesión", "icon": "logout", "on_press": self.cerrar_sesion, "roles": ["Administrador", "Backend", "Frontend", "Vendedor"]},
            ]

            # Filtrar las opciones según el rol del usuario
            filtered_items = [item for item in menu_items if self.user_role in item["roles"]]
            print(f"Rol del usuario: {self.user_role}, Opciones filtradas: {len(filtered_items)}")  # Depuración

            # Generar dinámicamente las opciones del menú
            rv.data = [
                {
                    "viewclass": "CustomOneLineIconListItem",
                    "text": item["text"],
                    "icon": item["icon"],
                    "on_press": item["on_press"],  # Pasar la acción al contenedor personalizado
                }
                for item in filtered_items
            ]
            rv.refresh_from_data()  # Forzar la actualización visual
            print(f"Menú generado con {len(rv.data)} elementos.")  # Depuración

        return root

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

        # Vaciar los contenedores dinámicos
        root = self.root
        if root:
            rv = root.ids.get("menu_recycleview", None)
            if rv:
                rv.data = []  # Vaciar los datos del RecycleView
                rv.refresh_from_data()  # Forzar la actualización visual
                print("RecycleView vaciado.")

        # Detener la aplicación actual
        self.stop()

        # Reiniciar el proceso de inicio de sesión
        login_app = LoginApp()
        login_app.run()

        # Si el inicio de sesión es exitoso, reiniciar la aplicación principal
        if login_app.valido:
            menu_app = MenuApp(self.kv_path, self.kv_file)
            menu_app.set_user_role(login_app.rol)
            menu_app.run()

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
        mostrar_opcion_en_desarrollo(self)
        """kv_file = 'pedidos.kv'
        self.stop()
        UserApp(KV_BASE_PATH, kv_file, self.kv_path, self.kv_file).run()"""

    def gestion_proveedores(self):
        """
        Navega a la pantalla de gestión de proveedores.
        """
        mostrar_opcion_en_desarrollo(self)
        """kv_file = 'proveedores.kv'
        self.stop()
        UserApp(KV_BASE_PATH, kv_file, self.kv_path, self.kv_file).run()
"""
    def gestion_articulos(self):
        """
        Navega a la pantalla de gestión de artículos.
        """
        mostrar_opcion_en_desarrollo(self)
        """kv_file = 'articulos.kv'
        self.stop()
        UserApp(KV_BASE_PATH, kv_file, self.kv_path, self.kv_file).run()"""

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
        self.height = "450dp"  # Ajustar la altura para incluir el checkbox

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

        # Botón para desplegar el menú de roles alineado a la izquierda
        self.rol_button = MDRaisedButton(
            text="Seleccionar Rol",
            size_hint_x=0.9,
            pos_hint={"x": 0},  # Alinear a la izquierda
            on_release=self.open_menu
        )
        self.add_widget(self.rol_button)

        # Checkbox para estado activo
        self.checkbox_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint_x=0.9,
            pos_hint={"center_x": 0.5},
        )
        self.checkbox = MDCheckbox(active=True)  # Por defecto, el usuario está activo
        self.checkbox_label = MDLabel(
            text="Activo",
            size_hint_x=None,
            halign="left",
        )
        self.checkbox_layout.add_widget(self.checkbox)
        self.checkbox_layout.add_widget(self.checkbox_label)
        self.add_widget(self.checkbox_layout)

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
            "nombre_usuario": content.children[5].text,
            "clave": content.children[4].text,
            "apellido": content.children[3].text,
            "nombre": content.children[2].text,
            "rol": content.rol_button.text,  # Obtener el texto del botón de rol
            "activo": content.checkbox.active,  # Obtener el estado del checkbox
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
        """
        Marca a un usuario como inactivo en lugar de eliminarlo.
        """
        try:
            # Obtener la lista de usuarios
            usuarios = ejecutar_operacion("usuarios", operacion="busqueda", condiciones="1=1")
            if not usuarios:
                print("No se encontraron usuarios.")
                return

            # Crear una lista para seleccionar el usuario a dar de baja
            lista_usuarios = MDList()
            for usuario in usuarios:
                if usuario[1].lower() == "root":  # Evitar dar de baja al usuario "root"
                    continue
                lista_usuarios.add_widget(
                    OneLineListItem(
                        text=f"ID: {usuario[0]}, Usuario: {usuario[1]}, Nombre: {usuario[4]} {usuario[3]}",
                        on_release=lambda _, u=usuario: self.confirmar_baja_usuario(u)  # Pasar los datos del usuario
                    )
                )

            # Crear el popup con la lista de usuarios
            self.dialog = MDDialog(
                title="Seleccionar Usuario para Dar de Baja",
                type="custom",
                content_cls=lista_usuarios,
                buttons=[
                    MDRaisedButton(
                        text="CERRAR",
                        on_release=lambda _: self.dialog.dismiss(),
                    ),
                ],
            )
            self.dialog.open()

        except Exception as e:
            print(f"Error al consultar usuarios: {e}")

    def confirmar_baja_usuario(self, usuario):
        """
        Confirma la baja del usuario seleccionado.
        """
        self.dialog.dismiss()  # Cerrar el popup de selección

        # Crear un diálogo de confirmación
        self.dialog = MDDialog(
            title=f"Dar de Baja Usuario: {usuario[1]}",
            text="¿Estás seguro de que deseas dar de baja a este usuario?",
            buttons=[
                MDRaisedButton(
                    text="CANCELAR",
                    on_release=lambda _: self.dialog.dismiss(),
                ),
                MDRaisedButton(
                    text="CONFIRMAR",
                    on_release=lambda _: self.realizar_baja_usuario(usuario[0]),
                ),
            ],
        )
        self.dialog.open()

    def realizar_baja_usuario(self, usuario_id):
        """
        Realiza la baja del usuario marcándolo como inactivo, excepto para el usuario "root".
        """
        try:
            # Verificar si el usuario es "root"
            usuario = ejecutar_operacion(
                "usuarios",
                operacion="busqueda",
                condiciones=f"id = {usuario_id}"
            )
            if usuario and usuario[0][1].lower() == "root":
                print("No se puede desactivar al usuario 'root'.")
                self.dialog.dismiss()
                return

            # Marcar al usuario como inactivo
            ejecutar_operacion(
                "usuarios",
                datos={"activo": False},
                operacion="modificacion",
                condiciones=f"id = {usuario_id}",
            )
            print(f"Usuario con ID {usuario_id} dado de baja exitosamente.")
        except Exception as e:
            print(f"Error al dar de baja al usuario: {e}")
        finally:
            self.dialog.dismiss()

    def modificacion_usuario(self):
        """
        Muestra un formulario para modificar un usuario existente.
        """
        try:
            # Obtener la lista de usuarios
            usuarios = ejecutar_operacion("usuarios", operacion="busqueda", condiciones="1=1")
            if not usuarios:
                print("No se encontraron usuarios.")
                return

            # Crear una lista para seleccionar el usuario a modificar
            lista_usuarios = MDList()
            for usuario in usuarios:
                lista_usuarios.add_widget(
                    OneLineListItem(
                        text=f"{usuario[0]} - {usuario[1]} ({usuario[4]})",
                        on_release=lambda _, u=usuario: self.mostrar_formulario_modificacion(u)  # Pasar los datos del usuario
                    )
                )

            # Crear el popup con la lista de usuarios
            self.dialog = MDDialog(
                title="Seleccionar Usuario",
                type="custom",
                content_cls=lista_usuarios,
                buttons=[
                    MDRaisedButton(
                        text="CERRAR",
                        on_release=lambda _: self.dialog.dismiss(),
                    ),
                ],
            )
            self.dialog.open()

        except Exception as e:
            print(f"Error al consultar usuarios: {e}")

    def mostrar_formulario_modificacion(self, usuario):
        """
        Muestra un formulario para modificar los datos del usuario seleccionado.
        """
        # Cerrar el diálogo anterior si existe
        if self.dialog:
            self.dialog.dismiss(force=True)

        # Crear el formulario de modificación como un MDBoxLayout
        formulario = MDBoxLayout(
            orientation="vertical",
            spacing=10,
            padding=10,
            size_hint_y=None,
            height="450dp",  # Ajustar la altura para incluir el checkbox
        )

        # Añadir campos al formulario
        formulario.add_widget(MDTextField(
            id="nombre_usuario",
            hint_text="Nombre de Usuario",
            text=usuario[1],
            required=True,
        ))
        formulario.add_widget(MDTextField(
            id="clave",
            hint_text="Clave",
            text=usuario[2],
            password=True,
            required=True,
        ))
        formulario.add_widget(MDTextField(
            id="apellido",
            hint_text="Apellido",
            text=usuario[3],
        ))
        formulario.add_widget(MDTextField(
            id="nombre",
            hint_text="Nombre",
            text=usuario[4],
        ))
        formulario.add_widget(MDTextField(
            id="rol",
            hint_text="Rol",
            text=usuario[5],
        ))

        # Checkbox para estado activo
        checkbox_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint_x=0.9,
            pos_hint={"center_x": 0.5},
        )
        checkbox = MDCheckbox(active=usuario[6] == 1 or usuario[6] is None)  # Determinar el estado inicial del checkbox
        checkbox_label = MDLabel(
            text="Activo",
            size_hint_x=None,
            halign="left",
        )
        checkbox_layout.add_widget(checkbox)
        checkbox_layout.add_widget(checkbox_label)
        formulario.add_widget(checkbox_layout)

        # Crear el popup con el formulario
        self.dialog = MDDialog(
            title=f"Modificar Usuario: {usuario[1]}",
            type="custom",
            content_cls=formulario,  # Asignar el formulario como contenido
            buttons=[
                MDRaisedButton(
                    text="CANCELAR",
                    on_release=lambda _: self.dialog.dismiss(),
                ),
                MDRaisedButton(
                    text="GUARDAR",
                    on_release=lambda _: self.guardar_modificacion_usuario(usuario[0]),
                ),
            ],
        )
        self.dialog.open()

    def guardar_modificacion_usuario(self, usuario_id):
        """
        Guarda los cambios realizados al usuario en la base de datos.
        """
        content = self.dialog.content_cls

        # Buscar el checkbox dentro del layout
        checkbox = None
        for child in content.children:
            if isinstance(child, MDBoxLayout):
                for subchild in child.children:
                    if isinstance(subchild, MDCheckbox):
                        checkbox = subchild
                        break
                if checkbox:
                    break

        # Verificar si el usuario es "root"
        usuario = ejecutar_operacion(
            "usuarios",
            operacion="busqueda",
            condiciones=f"id = {usuario_id}"
        )
        if usuario and usuario[0][1].lower() == "root" and not checkbox.active:
            # Mostrar mensaje en pantalla
            self.dialog.dismiss()
            self.dialog = MDDialog(
                title="Error",
                text="No se puede desactivar al usuario 'root'.",
                buttons=[
                    MDRaisedButton(
                        text="CERRAR",
                        on_release=lambda _: self.dialog.dismiss(),
                    ),
                ],
            )
            self.dialog.open()
            return

        datos_modificados = {
            "nombre_usuario": content.children[5].text,
            "clave": content.children[4].text,
            "apellido": content.children[3].text,
            "nombre": content.children[2].text,
            "rol": content.children[1].text,
            "activo": checkbox.active if checkbox else False,  # Obtener el estado del checkbox
        }

        try:
            ejecutar_operacion(
                "usuarios",
                datos=datos_modificados,
                operacion="modificacion",
                condiciones=f"id = {usuario_id}",
            )
            print(f"Usuario {usuario_id} modificado exitosamente.")
        except Exception as e:
            print(f"Error al modificar el usuario: {e}")
        finally:
            self.dialog.dismiss()

    def consulta_usuarios(self):
        """
        Consulta y muestra el listado de usuarios en una ventana emergente.
        """
        try:
            usuarios = ejecutar_operacion("usuarios", operacion="busqueda", condiciones="1=1")  # Consultar todos los usuarios
            if not usuarios:
                print("No se encontraron usuarios.")
                return

            # Crear una lista para mostrar los usuarios
            lista_usuarios = MDList()
            for usuario in usuarios:
                # Manejar valores None en el campo 'activo'
                estado = "Activo" if usuario[6] in [1, True, "1", None] else "Baja"
                lista_usuarios.add_widget(
                    OneLineListItem(
                        text=f"ID: {usuario[0]}, Usuario: {usuario[1]}, Nombre: {usuario[4]} {usuario[3]}, Estado: {estado}"
                    )
                )

            # Crear el popup con la lista de usuarios
            self.dialog = MDDialog(
                title="Listado de Usuarios",
                type="custom",
                content_cls=lista_usuarios,
                buttons=[
                    MDRaisedButton(
                        text="CERRAR",
                        on_release=lambda _: self.dialog.dismiss(),
                    ),
                ],
            )
            self.dialog.open()

        except Exception as e:
            print(f"Error al consultar usuarios: {e}")

    def regresar_menu(self):
        """
        Regresa al menú principal.
        """
        self.stop()  # Detener la aplicación actual
        MenuApp(self.menu_kv_path, self.menu_kv_file).run()  # Reiniciar la aplicación del menú principal

    def alta_articulo(self):
        mostrar_opcion_en_desarrollo(self)

    def consulta_articulos(self):
        mostrar_opcion_en_desarrollo(self)

    def modificacion_articulo(self):
        mostrar_opcion_en_desarrollo(self)

    def baja_articulo(self):
        mostrar_opcion_en_desarrollo(self)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        id_usuario = sys.argv[1]
        rol_usuario = sys.argv[2]
        kv_path = KV_BASE_PATH
        kv_file = 'menu.kv'
        mostrar_rol_usuario(id_usuario, rol_usuario, kv_path, kv_file)
    else:
        print("No se ha proporcionado el ID y el rol del usuario.")
