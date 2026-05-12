class Cuenta:
    def __init__(self, numero, saldo=0):
        self.numero = numero
        self.saldo = saldo

    def depositar(self, monto):
        self.saldo += monto

    def retirar(self, monto):
        if monto <= self.saldo:
            self.saldo -= monto
        else:
            print("Saldo insuficiente")

    def __str__(self):
        return f"Cuenta {self.numero} - Saldo: ${self.saldo}"