import sys
import os
import time
import platform  # Importar el módulo platform

# Agregar el directorio que contiene abm.py al PYTHONPATH
#sys.path.append(os.path.join(os.path.dirname(__file__), 'mobile_app', 'utils'))
#from abm import ejecutar_operacion
from utils.abm import ejecutar_operacion

# from windows.app.desktopMain import mostrar_rol_usuario

from sync import create_local_database, start_sync_thread, create_database_remota
from login import login  #agregado para poder loguear

# Determinar el sistema operativo
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

# Función para cargar las pantallas según el sistema operativo
def cargar_pantallas(os_type):
    if os_type == "Android":
        from mobile_app.kv.android import inicio as cargar_pantallas
    elif os_type == "Linux":
        from linux.main import inicio as cargar_pantallas
    elif os_type == "Windows":
        from gestion import inicio as cargar_pantallas, mostrar_rol_usuario
        #from windows.app.desktopMain import inicio as cargar_pantallas
    elif os_type == "iOS":
        from ios.main import    inicio as cargar_pantallas
    elif os_type == "macOS":
        from macos.main import inicio as cargar_pantallas
    else:
        raise ValueError("Sistema operativo no soportado.")
        
#def inicio(os_type):
    return cargar_pantallas( os_type)   

# debo utilizar el mismo nombre de la funcion para todos los sistemas operativos, solo deben cambiar los kv, la logica es la misma
# entonces solo varian los sistemas oprativos y las visualizaiones, debo traer los utils, conexiones a base de datos, etc
# y otros modulos comunes a una capeta raiz, y luego en cada sistema operativo traer los kv y las pantallas

# usar async como alternativa
# hacer hilo de seguimiento
#a = 0  # SOLO UTILZADA PARA HACER ALGUNAS VARIACIONES EN LAS PRUEBAS

if __name__ == "__main__":
    os_type = get_os()
    cargar_pantallas(os_type)
    #print(f"Ejecutando en: {os_type}")  # averigua que sistema operativo esta corriendo

    if os_type == "Unknown":
        print("Sistema operativo no reconocido. Finalizando aplicación.")
        sys.exit(1)

    create_database_remota()  # se crea base de datos si no existe en el servidor  // FUNCIONANDO OK
    create_local_database()  # Crear base de datos local si no existe // FUNCIONANDO OK

    valido, id_usuario, mensaje, rol = login()  # función de login

    if valido:
        #Frontsync_thread = start_sync_thread()  # Iniciar sincronización en segundo plano // FUNCIONANDO OK
        print(f"Bienvenido {mensaje}! Rol: {rol}")
        #print("Base de datos local creada y sincronización automática iniciada.")

        # Cargar las pantallas según el sistema operativo
        cargar_pantallas(os_type)  # Llamar a la función para cargar las pantallas
        #cargar_pantallas_func = cargar_pantallas(os_type)
        #cargar_pantallas_func(os_type)  # Llamar a la función para cargar las pantallas

        # Ejecución principal 
        try:
            while True:
                # Aca va el programa en ejecucion normal
                print("Aplicación principal en ejecución...") 
                mostrar_rol_usuario(id_usuario, rol)  # Enviar el id y el rol del usuario a la función mostrar_menu

                """a += 1
                print(f"vueltas {a}")
                time.sleep(7)  # Simula la ejecución del programa"""

        except KeyboardInterrupt:
            print("Finalizando aplicación...")
    else:
        print(f"Error: {mensaje}")

