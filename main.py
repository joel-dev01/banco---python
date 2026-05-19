from db import ( obtener_movimientos, 
                crear_tabla_movimientos, 
                crear_db,
                actualizar_saldo_db,
                buscar_movimientos ) 
from banco import Banco
from cuenta import Cuenta
from politicas import *

def menu():
    crear_tabla_movimientos()
    crear_db()
    banco = Banco()
    

    while True:
        print("\n--- MENU ---")
        print("1. Crear cuenta")
        print("2. Transferir")
        print("3. Ver historial")
        print("4. Ver cuentas")
        print("5. Borrar cuenta")
        print("6. Modificar saldo")
        print("7. Depositar")
        print("8. Filtrar historial")
        print("0. Salir")

        opcion = input("Elegí una opción: ")

        if opcion == "1":
            titular = input("Nombre: ")

            try:
                saldo = float(input("Saldo inicial: "))
            except ValueError:
                print("Saldo inválido")
                continue

            cuenta = Cuenta(
                titular,
                saldo,
                politicas=[ComisionFija(), Cashback()]
            )

            banco.agregar_cuenta(cuenta)
            
        
        elif opcion == "2":
            print("Cuenta origen:")
            c1 = banco.seleccionar_cuenta()
            
            print("Cuenta destino")
            c2 = banco.seleccionar_cuenta()
            
            if not c1 or not c2:
                continue
            
            try:
                monto = float(input("Monto: "))
            except ValueError:
                print("Monto invalido")
                continue
            if banco.transferir(c1.id, c2.id, monto):
                

                print("Transferencia realizada")
            else:
                
                print("Error en la transferencia")
        elif opcion == "3":
            cuenta = banco.seleccionar_cuenta()
            if  not cuenta:
                continue
            movimientos = obtener_movimientos(cuenta.id)
            
            
            if not movimientos:
                    print("No hay movimientos")
                    continue
        
        
            for tipo, monto, fecha in movimientos:
                
                print(f"{fecha} | {tipo} | ${monto}")
                        
                   

        elif opcion == "4":
            banco.listar_cuentas()

        elif opcion == "5":
            cuenta = banco.seleccionar_cuenta()
            if not cuenta:
                continue
           
            confirmar = input("¿Seguro? (s/n): ")
                
            if confirmar.lower() != "s":
                print("Operacion cancelada")
                continue
            if banco.eliminar_cuenta(cuenta.id):
                print("Cuenta eliminada")
            else:
                print("Error al eliminar")
            

        elif opcion == "6":
            
            cuenta = banco.seleccionar_cuenta()

            if cuenta:
                try:
                    nuevo_saldo = float(input("Nuevo saldo: "))
                except ValueError:
                    print("Saldo inválido")
                    continue

                if cuenta._actualizar_memoria(nuevo_saldo):
                    
                    actualizar_saldo_db(cuenta.id, nuevo_saldo)
                    print("Saldo actualizado en memoria y SQL")
                    
                else:
                    print("No se pudo actualizar")
            else:
                print("Cuenta no encontrada")
        elif opcion == "7":
            cuenta = banco.seleccionar_cuenta()
            if not cuenta:
                continue
            try:
                monto = float(input("Monto a depositar: "))
            except ValueError:
                print("Monto invalido")
                continue
            if cuenta.depositar(monto):
                print("Depósito realizado")
                

            else:
                print("No se pudo realizar el depósito")
            
        
        

        elif opcion == "8":
            cuenta = banco.seleccionar_cuenta()
            if not cuenta:
                continue

            print("1. Depositos")
            print("2. Retiros")
            print("3. Transferencias")
            print("4. Todos")

            filtro = input("Elegí tipo: ")

            tipo = None

            if filtro == "1":
                tipo = "deposito"
            elif filtro == "2":
                tipo = "retiro"
            elif filtro == "3":
                tipo = "transferencia_enviada"
            elif filtro == "4":
                tipo = None
            else:
                print("Opción inválida")
                continue

            fecha_desde = input("Desde (YYYY-MM-DD) o Enter: ") or None
            fecha_hasta = input("Hasta (YYYY-MM-DD) o Enter: ") or None

            try:
                monto_min = input("Monto mínimo o Enter: ")
                monto_min = float(monto_min) if monto_min else None

                monto_max = input("Monto máximo o Enter: ")
                monto_max = float(monto_max) if monto_max else None
            except ValueError:
                print("Monto inválido")
                continue

            movimientos = buscar_movimientos(
            cuenta.id,
            tipo,
            fecha_desde,
            fecha_hasta,
            monto_min,
            monto_max )

            if not movimientos:
                print("No hay resultados")
                continue

            for tipo, monto, fecha in movimientos:
                print(f"{fecha} | {tipo} | ${monto}")
             
         
        
        elif opcion == "0":
            break

menu()