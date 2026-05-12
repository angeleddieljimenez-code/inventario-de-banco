class Cliente:
    def __init__(self, id_cliente, nombre):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.cuentas = []
        self.creditos = []

    def agregar_cuenta(self, cuenta):
        self.cuentas.append(cuenta)

    def agregar_credito(self, credito):
        self.creditos.append(credito)

    def __str__(self):
        return f"Cliente: {self.nombre} (ID: {self.id_cliente})"
    