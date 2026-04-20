from banco import Banco
from cuenta import Cuenta
from politicas import *

def menu():
    banco = Banco()
    banco.cargar()

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
            banco.guardar()
        
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
                banco.guardar()
            else:
                print("Error en la transferencia")    
        elif opcion == "3":
            cuenta = banco.seleccionar_cuenta()
            if cuenta:
                
                historial = cuenta.ver_historial()

                if not historial:
                    print("No hay movimientos")
        
                else:
                    for mov in historial:
                        print(f"{mov['fecha']} | {mov['tipo']} | ${mov['monto']} | saldo: ${mov['saldo']}")
                        
                   

        elif opcion == "4":
            banco.listar_cuentas()

        elif opcion == "5":
            cuenta = banco.seleccionar_cuenta()
            if cuenta:
                banco.eliminar_cuenta(cuenta.id)
                banco.guardar()

        elif opcion == "6":
            
            cuenta = banco.seleccionar_cuenta()

            if cuenta:
                try:
                    nuevo_saldo = float(input("Nuevo saldo: "))
                except ValueError:
                    print("Saldo inválido")
                    continue

                if cuenta.actualizar_saldo(nuevo_saldo):
                    print("Saldo actualizado")
                    banco.guardar()
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
                print("Deposito realizado")
                banco.guardar()
            else:
                print("No se pudo realizar el deposito") 
        
        elif opcion == "8":
            cuenta = banco.seleccionar_cuenta()
            if not cuenta:
                continue
            historial = cuenta.ver_historial() 
            solo_depositos = [mov for mov in historial if mov["tipo"] == "deposito"]
            solo_retiros = [mov for mov in historial if mov["tipo"] == "retiro"]
            transferencias = [mov for mov in historial if mov["tipo"] in ["transferencia_enviada", "transferencia_recivida"]]
             
            print("1. - Depositos")
            print("2. - Retiros")
            print("3. - Tranferencias")
            
            filtro = input("Elegi una opcion: ")
            if filtro == "1":
                
                lista = solo_depositos
            elif filtro == "2":
                lista = solo_retiros
            elif filtro == "3":
                lista = transferencias
            
            else:
                print("Opcion invalida")
                continue
            for mov in lista:
                if not lista:
                    print("No hay movimientos de este tipo")
                    continue
                print(f"{mov['fecha']} | {mov['tipo']} | ${mov['monto']} | Saldo: ${mov['saldo']}")
             
            
        
        elif opcion == "0":
            break

menu()