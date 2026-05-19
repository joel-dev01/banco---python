from db import obtener_cuentas, insertar_cuenta, obtener_cuenta_por_id, transferir, eliminar_cuenta_db

from cuenta import Cuenta

RUTA = "data/cuentas.json"

class Banco:
    
            

    def agregar_cuenta(self, cuenta):
        
        if self.buscar_cuenta(cuenta.id):
            print("Cuenta ya existe")
            return
        insertar_cuenta(cuenta)
        

    def buscar_cuenta(self, id):
        fila = obtener_cuenta_por_id(id)
        if fila:
            return Cuenta(fila[1], fila[2], id=fila[0])
        return None
        

    

    def transferir(self, origen_id, destino_id, monto):
        
        return transferir(origen_id, destino_id, monto)

    def listar_cuentas(self):
        cuentas = obtener_cuentas()
        if not cuentas:
            
            print("No hay cuentas")
            return

        for id, titular, saldo in cuentas:
            print(f"ID: {id} | Titular: {titular} | Saldo: {saldo}")

    def eliminar_cuenta(self, cuenta_id):
        return eliminar_cuenta_db(cuenta_id)

    def seleccionar_cuenta(self):
        
        cuentas = obtener_cuentas()

        if not cuentas:
            print("No hay cuentas")
            return None

        for i, (id, titular, saldo) in enumerate(cuentas):
            print(f"{i} - {titular} | Saldo: {saldo}")

        try:
            opcion = int(input("Elegí una cuenta: "))
            id = cuentas[opcion][0]
            return self.buscar_cuenta(id)
        except (ValueError, IndexError):
            print("Opción inválida")
        return None
