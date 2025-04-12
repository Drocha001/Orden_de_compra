from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton

def mostrar_opcion_en_desarrollo(app):
    """
    Muestra una ventana emergente indicando que la opción está en desarrollo.
    
    :param app: Instancia de la aplicación actual para manejar el cierre del diálogo.
    """
    def cerrar_dialogo(*args):
        dialog.dismiss()  # Cierra el diálogo

    # Crear el diálogo
    dialog = MDDialog(
        title="Opción en Desarrollo",
        text="Esta opción aún no está disponible. Por favor, inténtelo más tarde.",
        buttons=[
            MDRaisedButton(
                text="Aceptar",
                on_release=cerrar_dialogo
            )
        ],
    )
    dialog.open()
