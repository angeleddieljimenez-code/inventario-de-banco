from banco.cliente import Cliente
from banco.cuenta import Cuenta
from banco.credito import Credito
from banco.inventario import InventarioBanco

banco = InventarioBanco()

# ===============================
# FUNCIONES DEL MENÚ
# ===============================

def crear_cliente():
    id_cliente = int(input("ID del cliente: "))
    nombre = input("Nombre: ")
    cliente = Cliente(id_cliente, nombre)
    banco.agregar_cliente(cliente)
    print("✅ Cliente agregado\n")


def agregar_cuenta():
    id_cliente = int(input("ID del cliente: "))
    cliente = banco.buscar_cliente(id_cliente)

    if cliente:
        numero = input("Número de cuenta: ")
        saldo = float(input("Saldo inicial: "))
        cuenta = Cuenta(numero, saldo)
        cliente.agregar_cuenta(cuenta)
        print("✅ Cuenta agregada\n")
    else:
        print("❌ Cliente no encontrado\n")


def agregar_credito():
    id_cliente = int(input("ID del cliente: "))
    cliente = banco.buscar_cliente(id_cliente)

    if cliente:
        id_credito = input("ID del crédito: ")
        monto = float(input("Monto total: "))
        deuda = float(input("Deuda actual: "))
        credito = Credito(id_credito, monto, deuda)
        cliente.agregar_credito(credito)
        print("✅ Crédito agregado\n")
    else:
        print("❌ Cliente no encontrado\n")


def depositar():
    id_cliente = int(input("ID del cliente: "))
    cliente = banco.buscar_cliente(id_cliente)

    if cliente:
        numero = input("Número de cuenta: ")
        for cuenta in cliente.cuentas:
            if cuenta.numero == numero:
                monto = float(input("Monto a depositar: "))
                cuenta.depositar(monto)
                print("✅ Depósito realizado\n")
                return
        print("❌ Cuenta no encontrada\n")
    else:
        print("❌ Cliente no encontrado\n")


def retirar():
    id_cliente = int(input("ID del cliente: "))
    cliente = banco.buscar_cliente(id_cliente)

    if cliente:
        numero = input("Número de cuenta: ")
        for cuenta in cliente.cuentas:
            if cuenta.numero == numero:
                monto = float(input("Monto a retirar: "))
                cuenta.retirar(monto)
                print("✅ Retiro realizado\n")
                return
        print("❌ Cuenta no encontrada\n")
    else:
        print("❌ Cliente no encontrado\n")


def pagar_credito():
    id_cliente = int(input("ID del cliente: "))
    cliente = banco.buscar_cliente(id_cliente)

    if cliente:
        id_credito = input("ID del crédito: ")
        for credito in cliente.creditos:
            if credito.id_credito == id_credito:
                cantidad = float(input("Cantidad a pagar: "))
                credito.pagar(cantidad)
                print("✅ Pago realizado\n")
                return
        print("❌ Crédito no encontrado\n")
    else:
        print("❌ Cliente no encontrado\n")


def mostrar():
    print("\n📊 INVENTARIO DEL BANCO")
    banco.mostrar_inventario()
    print()


# ===============================
# MENÚ PRINCIPAL
# ===============================

def menu():
    while True:
        print("===== BANCO =====")
        print("1. Crear cliente")
        print("2. Agregar cuenta")
        print("3. Agregar crédito")
        print("4. Depositar")
        print("5. Retirar")
        print("6. Pagar crédito")
        print("7. Mostrar inventario")
        print("0. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            crear_cliente()
        elif opcion == "2":
            agregar_cuenta()
        elif opcion == "3":
            agregar_credito()
        elif opcion == "4":
            depositar()
        elif opcion == "5":
            retirar()
        elif opcion == "6":
            pagar_credito()
        elif opcion == "7":
            mostrar()
        elif opcion == "0":
            print("👋 Saliendo del sistema...")
            break
        else:
            print("❌ Opción inválida\n")


# Ejecutar sistema
menu()
banco = InventarioBanco()
banco.cargar_datos()
