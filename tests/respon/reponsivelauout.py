from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
import os


class CommonComponentLabel(MDLabel):
    pass


class MobileView(MDScreen):
    pass


class TabletView(MDScreen):
    pass


class DesktopView(MDScreen):
    pass


class ResponsiveView(MDResponsiveLayout, MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.mobile_view = MobileView()
        self.tablet_view = TabletView()
        self.desktop_view = DesktopView()


class Test(MDApp):
    def build(self):
        # Ejecutar maximizado de la ventana
        #Window.maximize()
        # Establecer el tamaño mínimo de la ventana (valores mayores a 0)
        Window.minimum_width = 400  # Ancho mínimo
        Window.minimum_height = 300  # Alto mínimo

        # Vincular el evento de cambio de tamaño de la ventana
        Window.bind(on_resize=self.on_window_resize)

        # Cargar el archivo KV externo
        kv_file = os.path.join('models', 'pantallas.kv')  # Asegúrate de que la ruta sea correcta
        if not os.path.exists(kv_file):
            raise FileNotFoundError(f"El archivo {kv_file} no existe.")
        return Builder.load_file(kv_file)

    def on_window_resize(self, window, width, height):
        
        #Detecta cambios en el tamaño de la ventana y ajusta la interfaz según la orientación.
       
        if width > height:
            print("Pantalla en modo horizontal")
            # Aquí puedes ajustar la interfaz para modo horizontal
        else:
            print("Pantalla en modo vertical")
            # Aquí puedes ajustar la interfaz para modo vertical


Test().run()