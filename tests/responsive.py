from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window

class MobileView(MDScreen):
    pass

class TabletView(MDScreen):
    pass

class DesktopView(MDScreen):
    pass

class ResponsiveView(MDResponsiveLayout, MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mobile_view = MobileView()
        self.tablet_view = TabletView()
        self.desktop_view = DesktopView()
        self.current_view = None  # Para rastrear la vista actual
        self.detect_screen_size()

    def detect_screen_size(self):
        width, height = Window.size
        print(f"Tamaño actual de la ventana: {width}x{height}")  # Depuración

        # Determinar la vista según el tamaño de la ventana
        if width <= 600:
            self.switch_view(self.mobile_view, "Dispositivo: Móvil")
        elif width <= 1200:
            self.switch_view(self.tablet_view, "Dispositivo: Tableta")
        else:
            self.switch_view(self.desktop_view, "Dispositivo: Escritorio")

    def switch_view(self, new_view, message):
        # Eliminar la vista actual si existe
        if self.current_view:
            self.remove_widget(self.current_view)

        # Agregar la nueva vista
        self.current_view = new_view
        self.add_widget(self.current_view)
        print(message)  # Mostrar el tipo de dispositivo en la consola

class Test(MDApp):
    def build(self):
        # Maximizar la ventana al iniciar
        Window.maximize()

        # Cargar el archivo KV
        Builder.load_file('f:\\python\\kivy\\Orden de compra\\tests\\res.kv')
        return ResponsiveView()

Test().run()