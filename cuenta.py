from datetime import datetime
import uuid




# ---------------- CUENTA ----------------

class Cuenta:
    def __init__(self, titular, saldo, politicas=None, id=None):
        self.id = id if id else str(uuid.uuid4())
        self.titular = titular
        self._saldo = saldo
        self._politicas = politicas if politicas else []
        self._historial = []

    @property
    def saldo(self):
        return self._saldo

    def depositar(self, monto):
        if monto <= 0:
            return False
        self._saldo += monto
        self._registrar_movimiento("deposito", monto)
        return True

    def retirar(self, monto):
        for politica in self._politicas:
            if hasattr(politica, "permitir"):
                if not politica.permitir(self, monto):
                    return False

        total = monto
        for politica in self._politicas:
            if hasattr(politica, "calcular"):
                total += politica.calcular(self, monto)

        if total <= 0 or total > self._saldo:
            return False

        self._saldo -= total
        self._registrar_movimiento("retiro", total)
        
        return True

    def transferir(self, otra_cuenta, monto):
        if self.retirar(monto):
            otra_cuenta.depositar(monto)
            
            
            self._registrar_movimiento("transferencia_enviada", monto)
    
            otra_cuenta._registrar_movimiento("transferencia_recibida", monto)
            
            
            return True
        return False

    def actualizar_saldo(self, nuevo_saldo):
        if nuevo_saldo < 0:
            return False
        saldo_anterior = self._saldo
        self._saldo = nuevo_saldo
        self._historial.append({
            "tipo": "ajuste",
            "antes": saldo_anterior,
            "despues": nuevo_saldo,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "saldo": self._saldo })
        
        return True

    def ver_historial(self):
        return self._historial

    def __str__(self):
        return f"Titular: {self.titular} - Saldo: {self._saldo}"
    
    def _registrar_movimiento(self, tipo, monto):
        movimiento = {
            "tipo": tipo,
            "monto": monto,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"
            ),
            "saldo": self._saldo 
        }
        self._historial.append(movimiento)