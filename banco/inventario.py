from banco.cliente import Cliente

class InventarioBanco:
    def __init__(self):
        self.clientes = []

    def agregar_cliente(self, cliente):
        self.clientes.append(cliente)

    def buscar_cliente(self, id_cliente):
        for c in self.clientes:
            if c.id_cliente == id_cliente:
                return c
        return None

    def mostrar_inventario(self):
        for cliente in self.clientes:
            print(cliente)
            for cuenta in cliente.cuentas:
                print("  ", cuenta)
            for credito in cliente.creditos:
                print("  ", credito)
                import json
                