import json
from cuenta import Cuenta

RUTA = "data/cuentas.json"

class Banco:
    def __init__(self):
        self.cuentas = []

    def agregar_cuenta(self, cuenta):
        
        if self.buscar_cuenta(cuenta.id):
            print("Cuenta ya existe")
            return
        self.cuentas.append(cuenta)

    def buscar_cuenta(self, id):
        for cuenta in self.cuentas:
            if cuenta.id == id:
                return cuenta
        return None

    def transferir(self, origen_id, destino_id, monto):
        c1 = self.buscar_cuenta(origen_id)
        c2 = self.buscar_cuenta(destino_id)

        if c1 and c2:
            return c1.transferir(c2, monto)
        return False

    def listar_cuentas(self):
        if not self.cuentas:
            print("No hay cuentas")
            return
        for cuenta in self.cuentas:
            print(f"ID: {cuenta.id} | {cuenta}")

    def eliminar_cuenta(self, id):
        cuenta = self.buscar_cuenta(id)
        if cuenta:
            self.cuentas.remove(cuenta)
            print("Cuenta eliminada")
            return True
        print("Cuenta no encontrada")
        return False

    def seleccionar_cuenta(self):
        if not self.cuentas:
            print("No hay cuentas")
            return None
        for i, cuenta in enumerate(self.cuentas):
            print(f"{i} - {cuenta.titular} Saldo: {cuenta.saldo}")
        try:
            opcion = int(input("Elegí una cuenta: "))
            return self.cuentas[opcion]
        except (ValueError, IndexError):
            print("Opción inválida")
            return None

    def guardar(self):
        datos = []
        for cuenta in self.cuentas:
            datos.append({
                "id": cuenta.id,
                "titular": cuenta.titular,
                "saldo": cuenta.saldo,
                "historial": cuenta.ver_historial()
            })

        with open(RUTA, "w") as archivo:
            json.dump(datos, archivo, indent=4)

    def cargar(self):
        try:
            with open(RUTA, "r") as archivo:
                datos = json.load(archivo)

            for item in datos:
                cuenta = Cuenta(
                    item["titular"],
                    item["saldo"],
                    id=item.get("id")
                )
                cuenta._historial = item["historial"]
                self.cuentas.append(cuenta)

        except FileNotFoundError:
            print("No hay datos guardados")