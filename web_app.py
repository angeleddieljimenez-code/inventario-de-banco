# web_app.py COMPLETO
from flask import Flask, render_template, request, redirect, session
import sqlite3
import random
from datetime import datetime

app = Flask(__name__)

app.secret_key = 'supersecretkey'

# =========================
# CREAR BASE DE DATOS
# =========================

def crear_bd():

    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()

    # TABLA USUARIOS

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL
        )
    ''')

    # TABLA ADMINS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute(
        "SELECT * FROM admins WHERE usuario = ?",
        ('admin',)
    )

    admin = cursor.fetchone()

    if not admin:
        cursor.execute(
            '''
            INSERT INTO admins(usuario, password)
            VALUES(?, ?)
            ''',
            ('admin', 'FIME2027')
        )

    # TABLA INVENTARIO
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventario(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto TEXT NOT NULL,
            cantidad INTEGER NOT NULL
        )
    ''')

    # TABLA CUENTAS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cuentas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT NOT NULL,
            saldo REAL NOT NULL,
            tarjeta TEXT NOT NULL
        )
    ''')

    # TABLA MOVIMIENTOS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movimientos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cuenta TEXT NOT NULL,
            tipo TEXT NOT NULL,
            cantidad REAL NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conexion.commit()
    conexion.close()

crear_bd()

# =========================
# PAGINA PRINCIPAL
# =========================

@app.route('/')
def inicio():

    return render_template('index.html')

# =========================
# LOGIN
# =========================

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        usuario = request.form['usuario']
        password = request.form['password']

        conexion = sqlite3.connect('database.db')
        cursor = conexion.cursor()

        cursor.execute(
            '''
            SELECT * FROM admins
            WHERE usuario = ? AND password = ?
            ''',
            (usuario, password)
        )

        admin = cursor.fetchone()

        conexion.close()

        if admin:

            session['usuario'] = usuario

            return redirect('/dashboard')

    return render_template('login.html')

# =========================
# LOGOUT
# =========================

@app.route('/logout')
def logout():

    session.pop('usuario', None)

    return redirect('/login')

# =========================
# DASHBOARD
# =========================

@app.route('/dashboard')
def dashboard():

    if 'usuario' not in session:
        return redirect('/login')

    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()

    # USUARIOS

    cursor.execute(
        "SELECT COUNT(*) FROM usuarios"
    )

    total_usuarios = cursor.fetchone()[0]

    # CUENTAS

    cursor.execute(
        "SELECT COUNT(*) FROM cuentas"
    )

    total_cuentas = cursor.fetchone()[0]

    # DINERO TOTAL

    cursor.execute(
        "SELECT SUM(saldo) FROM cuentas"
    )

    total_dinero = cursor.fetchone()[0]

    if total_dinero is None:
        total_dinero = 0

    # MOVIMIENTOS

    cursor.execute(
        "SELECT COUNT(*) FROM movimientos"
    )

    total_movimientos = cursor.fetchone()[0]

    conexion.close()

    return render_template(
        'dashboard.html',
        total_usuarios=total_usuarios,
        total_cuentas=total_cuentas,
        total_dinero=total_dinero,
        total_movimientos=total_movimientos
    )
    
# =========================
# USUARIOS
# =========================

@app.route('/usuarios')
def usuarios():

    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM usuarios")

    usuarios = cursor.fetchall()

    conexion.close()

    return render_template(
        'usuarios.html',
        usuarios=usuarios
    )

# =========================
# ELIMINAR USUARIO
# =========================

@app.route('/eliminar_usuario/<int:id>')
def eliminar_usuario(id):

    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM usuarios WHERE id = ?",
        (id,)
    )

    conexion.commit()
    conexion.close()

    return redirect('/usuarios')

# =========================
# AGREGAR USUARIO
# =========================

@app.route('/agregar', methods=['POST'])
def agregar():

    nombre = request.form['nombre']
    correo = request.form['correo']

    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO usuarios(nombre, correo) VALUES(?, ?)",
        (nombre, correo)
    )

    conexion.commit()
    conexion.close()

    return redirect('/usuarios')

# =========================
# INVENTARIO
# =========================

@app.route('/inventario')
def inventario():

    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT * FROM inventario"
    )

    productos = cursor.fetchall()

    conexion.close()

    return render_template(
        'inventario.html',
        productos=productos
    )

# =========================
# AGREGAR PRODUCTO
# =========================

@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():

    producto = request.form['producto']
    cantidad = request.form['cantidad']

    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()

    cursor.execute(
        '''
        INSERT INTO inventario(producto, cantidad)
        VALUES(?, ?)
        ''',
        (producto, cantidad)
    )

    conexion.commit()
    conexion.close()

    return redirect('/inventario')

# =========================
# ELIMINAR PRODUCTO
# =========================

@app.route('/eliminar_producto/<int:id>')
def eliminar_producto(id):

    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM inventario WHERE id = ?",
        (id,)
    )

    conexion.commit()
    conexion.close()

    return redirect('/inventario')

# =========================
# CUENTAS
# =========================

@app.route('/cuentas')
def cuentas():

    buscar = request.args.get('buscar')

    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()

    if buscar:

        cursor.execute(
            '''
            SELECT * FROM cuentas
            WHERE cliente LIKE ?
            ''',
            ('%' + buscar + '%',)
        )

    else:

        cursor.execute(
            "SELECT * FROM cuentas"
        )

    cuentas = cursor.fetchall()

    conexion.close()

    return render_template(
        'cuentas.html',
        cuentas=cuentas
    )

# =========================
# CREAR CUENTA
# =========================

@app.route('/crear_cuenta', methods=['POST'])
def crear_cuenta():

    cliente = request.form['cliente']
    saldo = request.form['saldo']

    tarjeta = str(
        random.randint(
            1000000000000000,
            9999999999999999
        )
    )

    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()

    cursor.execute(
        '''
        INSERT INTO cuentas(cliente, saldo, tarjeta)
        VALUES(?, ?, ?)
        ''',
        (cliente, saldo, tarjeta)
    )

    conexion.commit()
    conexion.close()

    return redirect('/cuentas')

# =========================
# DEPOSITAR
# =========================

@app.route('/depositar/<int:id>', methods=['POST'])
def depositar(id):

    cantidad = float(request.form['cantidad'])

    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT saldo FROM cuentas WHERE id = ?",
        (id,)
    )

    saldo_actual = cursor.fetchone()[0]

    nuevo_saldo = saldo_actual + cantidad

    cursor.execute(
        '''
        UPDATE cuentas
        SET saldo = ?
        WHERE id = ?
        ''',
        (nuevo_saldo, id)
    )

    # GUARDAR MOVIMIENTO

    cursor.execute(
        '''
        INSERT INTO movimientos(cuenta, tipo, cantidad)
        VALUES(?, ?, ?)
        ''',
        (id, 'Deposito', cantidad)
    )

    conexion.commit()
    conexion.close()

    return redirect(
    f'/recibo/Deposito/{cantidad}'
)

# =========================
# RETIRAR
# =========================

@app.route('/retirar/<int:id>', methods=['POST'])
def retirar(id):

    cantidad = float(request.form['cantidad'])

    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT saldo FROM cuentas WHERE id = ?",
        (id,)
    )

    saldo_actual = cursor.fetchone()[0]

    if saldo_actual >= cantidad:

        nuevo_saldo = saldo_actual - cantidad

        cursor.execute(
            '''
            UPDATE cuentas
            SET saldo = ?
            WHERE id = ?
            ''',
            (nuevo_saldo, id)
        )

        # GUARDAR MOVIMIENTO

        cursor.execute(
            '''
            INSERT INTO movimientos(cuenta, tipo, cantidad)
            VALUES(?, ?, ?)
            ''',
            (id, 'Retiro', cantidad)
        )

        conexion.commit()

    conexion.close()

    return redirect(
    f'/recibo/Retiro/{cantidad}'
)
# =========================
# TRANSFERENCIAS
# =========================

@app.route('/transferir', methods=['POST'])
def transferir():

    origen = request.form['origen']
    destino = request.form['destino']
    cantidad = float(request.form['cantidad'])

    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT saldo FROM cuentas WHERE id = ?",
        (origen,)
    )

    saldo_origen = cursor.fetchone()[0]

    if saldo_origen >= cantidad:

        nuevo_origen = saldo_origen - cantidad

        cursor.execute(
            '''
            UPDATE cuentas
            SET saldo = ?
            WHERE id = ?
            ''',
            (nuevo_origen, origen)
        )

        cursor.execute(
            "SELECT saldo FROM cuentas WHERE id = ?",
            (destino,)
        )

        saldo_destino = cursor.fetchone()[0]

        nuevo_destino = saldo_destino + cantidad

        cursor.execute(
            '''
            UPDATE cuentas
            SET saldo = ?
            WHERE id = ?
            ''',
            (nuevo_destino, destino)
        )

        # MOVIMIENTOS

        cursor.execute(
            '''
            INSERT INTO movimientos(cuenta, tipo, cantidad)
            VALUES(?, ?, ?)
            ''',
            (origen, 'Transferencia Enviada', cantidad)
        )

        cursor.execute(
            '''
            INSERT INTO movimientos(cuenta, tipo, cantidad)
            VALUES(?, ?, ?)
            ''',
            (destino, 'Transferencia Recibida', cantidad)
        )

        conexion.commit()

    conexion.close()

    return redirect(
    f'/recibo/Transferencia/{cantidad}'
)

# =========================
# MOVIMIENTOS
# =========================

@app.route('/movimientos')
def movimientos():

    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()

    cursor.execute(
        '''
        SELECT * FROM movimientos
        ORDER BY fecha DESC
        '''
    )

    movimientos = cursor.fetchall()

    conexion.close()

    return render_template(
        'movimientos.html',
        movimientos=movimientos
    )

# =========================
# ELIMINAR CUENTA
# =========================

@app.route('/eliminar_cuenta/<int:id>')
def eliminar_cuenta(id):

    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM cuentas WHERE id = ?",
        (id,)
    )

    conexion.commit()
    conexion.close()

    return redirect('/cuentas')

# =========================
# RECIBO
# =========================

@app.route('/recibo/<tipo>/<cantidad>')
def recibo(tipo, cantidad):

    fecha = datetime.now().strftime(
        '%d/%m/%Y %H:%M:%S'
    )

    return render_template(
        'recibo.html',
        tipo=tipo,
        cantidad=cantidad,
        fecha=fecha
    )

# =========================
# ABONAR INVENTARIO
# =========================

@app.route('/abonar_producto/<int:id>', methods=['POST'])
def abonar_producto(id):

    cantidad = int(
        request.form['cantidad']
    )

    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()

    cursor.execute(
        '''
        SELECT cantidad
        FROM inventario
        WHERE id = ?
        ''',
        (id,)
    )

    actual = cursor.fetchone()[0]

    nueva = actual + cantidad

    cursor.execute(
        '''
        UPDATE inventario
        SET cantidad = ?
        WHERE id = ?
        ''',
        (nueva, id)
    )

    conexion.commit()
    conexion.close()

    return redirect('/inventario')

# =========================
# RESTAR INVENTARIO
# =========================

@app.route('/restar_producto/<int:id>', methods=['POST'])
def restar_producto(id):

    cantidad = int(
        request.form['cantidad']
    )

    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()

    cursor.execute(
        '''
        SELECT cantidad
        FROM inventario
        WHERE id = ?
        ''',
        (id,)
    )

    actual = cursor.fetchone()[0]

    nueva = actual - cantidad

    if nueva < 0:
        nueva = 0

    cursor.execute(
        '''
        UPDATE inventario
        SET cantidad = ?
        WHERE id = ?
        ''',
        (nueva, id)
    )

    conexion.commit()
    conexion.close()

    return redirect('/inventario')

# =========================
# EJECUTAR SERVIDOR
# =========================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
