
#import threading
import time
from abm import ejecutar_operacion
from sync import create_local_database, start_sync_thread,create_database_remota
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../mobile_app/utils'))
# usar async como alternativa
# hacer hilo de seguimiento
a=0  # SOLO UTILZADA PARA HACER ALGUNAS VARIACIONE EN LAS PRUEBAS

if __name__ == "__main__":
    create_database_remota() # se crea base de datos si no existe en el servidor  // FUNCIONANDO OK
    create_local_database()  # Crear base de datos local si no existe // FUNCIONANDO OK
    sync_thread = start_sync_thread()  # Iniciar sincronización en segundo plano // FUNCIONANDO OK

    print("Base de datos local creada y sincronización automática iniciada.")
    
    # Ejecución principal 
    try:
        while True:
            # Aca va el programa en ejecucion normal
            print("Aplicación principal en ejecución...")     

            """ ejemplo """
 
            """nuevo_articulo = {
                "id": None,  # Si es autoincremental, se puede omitir
                "descripcion": "MATE DE ACERO",
                "rubro": a,
                "stock": 25.77+a
            }"""

            articulo1 = {
                        #"id": None,
                        "descripcion": "modificacion Teclado inalámbrico",
                        "rubro": 1,
                        "stock": 150
                    }
            articulo2={
                        #"id": None,
                        "descripcion": "modificacionMouse óptico",
                        "rubro": 1,
                        "stock": 200
                    }
            articulo3={
                        #"id": None,
                        "descripcion": " modificacion aMonitor 24\ ",
                        "rubro": 2,
                        "stock": 50
                    }
            rub1= {
                    #"id": None,
                    "descripcion": "modificacion Nueva funcion unificadaPeriféricos"
                }
            cl={
                    #"id": None,
                    "nombre": "modificacion Nueva funcion unificada Juan Pérez",
                    "dni": 2034521354,
                    "domicilio": "Av. Rivadavia 3500",
                    "localidad": "Buenos Aires",
                    "provincia": "Buenos Aires",
                    "telefono": 1123456789,
                    "mail": "juanperez@gmail.com",
                    "activo": True
                }
            ped= {
                #"id": None,
                "proveedor": 1,
                "comprador": 1,
                "domicilio": "bv bsas",
                "viajante": "modificacion Nueva funcion unificada Carlos Gómez",
                "iva": "21%",
                "cuit": 3071000035,
                "vencimiento": "2025-03-20",
                "articulo": 1,
                "descripcion": "Teclado inalámbrico",
                "cantidad": 10,
                "precio_unitario": 3500,
                "total_art": 35000,
                "plan_entrega": "2025-03-25",
                "percepcion_iva": 7350,
                "subtotal1": 35000,
                "percepcion_ing_brutos": 500,
                "desrec": 0,
                "percepcion_ganancias": 0,
                "subtotal2": 40200,
                "percepcion_municipal": 300,
                "impuesto": 200,
                "otras_percepciones": 0,
                "total_pedido": 40700,
                "observaciones": "Entrega en 7 días",
                "forma_pago": "Transferencia"
            }
            prov={
                    #"id": None,
                    "nombre": "modificacion Nueva funcion unificada Distribuciones ABC",
                    "cuit": 2034521436,
                    "domicilio": "Calle Ficticia 1450",
                    "localidad": "Buenos Aires",
                    "provincia": "Buenos Aires",
                    "empresa": "ABC S.A.",
                    "telefono": 1122334455,
                    "mail": "contacto@abcsa.com.ar",
                    "activo": True
                }
            srub= {
                    #"id": None,
                    "descripcion": "modificacion Nueva funcion unificada Teclados"
                }
           

            # vamos a comentar para cuidar recursos mientras codificamos
            ejecutar_operacion("articulos", datos=articulo1, operacion='alta')
            #ejecutar_operacion("articulos", datos=articulo2, operacion='alta')
            #ejecutar_operacion("articulos", datos=articulo3, operacion='alta')  
            #ejecutar_operacion("rubro", rub1, operacion='alta')
            #ejecutar_operacion("clientes", cl, operacion='alta')   
            #ejecutar_operacion("proveedores", prov, operacion='alta')
            #ejecutar_operacion("subrubro", srub, operacion='alta')
            #ejecutar_operacion("pedidos", ped, operacion='alta')

            # Baja
            """print(ejecutar_operacion("articulos", operacion='baja', condiciones="id = 1"))
            print(ejecutar_operacion("rubro", operacion='baja', condiciones="id = 2"))
            print(ejecutar_operacion("clientes", operacion='baja', condiciones="id = 1"))
            print(ejecutar_operacion("proveedores", operacion='baja', condiciones="id = 1"))
            print(ejecutar_operacion("subrubro", operacion='baja', condiciones="id = 1"))
            print(ejecutar_operacion("pedidos", operacion='baja', condiciones="id = 1"))
            print(ejecutar_operacion("pedidos", operacion='baja', condiciones="id = 2"))"""
            
            # Modificación  le comente # "id": None, para que no de error la consulta solo valido para modificaion
            
            # print(ejecutar_operacion("articulos", datos=datos_modificados, operacion='modificacion', condiciones="id = 1"))
            #datos_modificados = {"descripcion": "DAME BOLA Laptop Gamer Pro", "stock": 45.0}
            #print(ejecutar_operacion("articulos",{"descripcion": "NO ME DES  BOLA Laptop Gamer Pro", "stock": 45.0}, operacion='modificacion', condiciones="id = 4"))
            """print(ejecutar_operacion("articulos",articulo1, operacion='modificacion', condiciones="id = 4"))
            print(ejecutar_operacion("rubro",rub1, operacion='modificacion', condiciones="id = 4"))
            print(ejecutar_operacion("clientes",cl, operacion='modificacion', condiciones="id = 4"))  
            print(ejecutar_operacion("proveedores",prov, operacion='modificacion', condiciones="id = 4"))
            print(ejecutar_operacion("subrubro",srub, operacion='modificacion', condiciones="id = 4"))    
            print(ejecutar_operacion("pedidos",ped, operacion='modificacion', condiciones="id = 4"))
            print(ejecutar_operacion("pedidos",ped, operacion='modificacion', condiciones="id = 4"))"""

            # Búsqueda
            """print(ejecutar_operacion("articulos", operacion='busqueda', condiciones="rubro = 4"))
            print(ejecutar_operacion("rubro", operacion='busqueda', condiciones="id = 4"))
            print(ejecutar_operacion("clientes", operacion='busqueda', condiciones="id = 4"))
            print(ejecutar_operacion("proveedores", operacion='busqueda', condiciones="id = 4"))
            print(ejecutar_operacion("subrubro", operacion='busqueda', condiciones="id = 4"))
            print(ejecutar_operacion("pedidos", operacion='busqueda', condiciones="id = 4"))"""




            a=a+1
            print (f"vueltas {a}")
            time.sleep(7)  # Simula la ejecución del programa

    except KeyboardInterrupt:
        print("Finalizando aplicación...")

