class Credito:
    def __init__(self, id_credito, monto, deuda):
        self.id_credito = id_credito
        self.monto = monto
        self.deuda = deuda

    def pagar(self, cantidad):
        self.deuda -= cantidad
        if self.deuda < 0:
            self.deuda = 0

    def __str__(self):
        return f"Crédito {self.id_credito} - Deuda: ${self.deuda}"