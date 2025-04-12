import sys
import os
from datos.vers.ver import verRes  
# Importa la función carpeta datos/vers/ver.py  importa las funcion verRes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


# ver()


a = verRes()  # Llamada correcta
print(a)
