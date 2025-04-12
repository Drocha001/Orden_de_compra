import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

# ID DE USUARIO, DEBE USARSE PARA GUARDAR EN LA BASE DE DATOS EL VENDEDOR, COMPRAODR, ETC, Y SE 
# UTILIZARA ESTE ID COMO RESTRICCION PARA QUE UN USUARIO NO PUEDA VER LO QUE HIZO OTRO
def inicio(os_type):
    print(f" H O L A   {os_type}")

def mostrar_rol_usuario(id_usuario, rol):
    print(f"-----> El rol del usuario es: {rol}, ID del usuario: {id_usuario}")
    
    if rol == "Administrador":
        print("Permisos: Puede hacer todo.")
        gestionar_todo(id_usuario)
        MenuApp().run()  # Ejecutar el menú solo para el administrador
    elif rol == "Backend":
        print("Permisos: Puede gestionar pedidos.")
        gestionar_pedidos(id_usuario)
    elif rol == "Frontend":
        print("Permisos: Puede dar de alta sus pedidos, borrar y modificar los que haya creado.")
        gestionar_pedidos_propios(id_usuario)
    elif rol == "Vendedor":
        print("Permisos: Puede cargar pedidos de ventas, ABM solo los creados con su usuario.")
        gestionar_pedidos_ventas(id_usuario)
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

class MenuApp(App):
    def build(self):
        return Builder.load_file('windows/app/models/menu.kv')# carpeta para buscar el kv

    def menu_opcion(self, opcion):
        print(f"Opción seleccionada: {opcion}")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        id_usuario = sys.argv[1]
        rol_usuario = sys.argv[2]
        mostrar_rol_usuario(id_usuario, rol_usuario)
    else:
        print("No se ha proporcionado el ID y el rol del usuario.")