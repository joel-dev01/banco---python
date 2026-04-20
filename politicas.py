
class ComisionFija:
    def __init__(self, comision=100):
        self.comision = comision

    def calcular(self, cuenta, monto):
        return self.comision if monto > 1000 else 0


class Cashback:
    def __init__(self, porcentaje=0.01):
        self.porcentaje = porcentaje

    def calcular(self, cuenta, monto):
        return -(monto * self.porcentaje)


class LimiteRetiro:
    def __init__(self, limite=2000):
        self.limite = limite

    def permitir(self, cuenta, monto):
        return monto <= self.limite


class SaldoMinimo:
    def __init__(self, minimo=1000):
        self.minimo = minimo

    def permitir(self, cuenta, monto):
        return (cuenta.saldo - monto) >= self.minimo
