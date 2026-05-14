from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# =========================
# CREAR BASE DE DATOS
# =========================

def crear_bd():

    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    # TABLA ADMINS

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
            ('admin', 'FIME2026')
        )

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventario(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto TEXT NOT NULL,
            cantidad INTEGER NOT NULL
        )
    ''')

    conexion.commit()
    conexion.close()

crear_bd()



# =========================
# INICIO
# =========================

@app.route('/')
def inicio():

    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()

    conexion.close()

    return render_template(
        'index.html',
        usuarios=usuarios
    )

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
# DASHBOARD
# =========================

@app.route('/dashboard')
def dashboard():

    if 'usuario' not in session:
        return redirect('/login')

    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM usuarios"
    )

    total_usuarios = cursor.fetchone()[0]

    conexion.close()

    return render_template(
        'dashboard.html',
        total_usuarios=total_usuarios
    )

# =========================
# USUARIOS
# =========================


@app.route('/usuarios')
def usuarios():

    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM usuarios")
    lista_usuarios = cursor.fetchall()

    conexion.close()

    return render_template(
        'usuarios.html',
        usuarios=lista_usuarios
    )

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
# REPORTES
# =========================

@app.route('/reportes')
def reportes():
    return render_template('reportes.html')

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
# ELIMINAR USUARIO
# =========================

@app.route('/eliminar/<int:id>')
def eliminar(id):

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
# EDITAR USUARIO
# =========================

@app.route('/editar/<int:id>')
def editar(id):

    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE id = ?",
        (id,)
    )

    usuario = cursor.fetchone()

    conexion.close()

    return render_template(
        'editar.html',
        usuario=usuario
    )


# =========================
# ACTUALIZAR USUARIO
# =========================

@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):

    nombre = request.form['nombre']
    correo = request.form['correo']

    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()

    cursor.execute(
        '''
        UPDATE usuarios
        SET nombre = ?, correo = ?
        WHERE id = ?
        ''',
        (nombre, correo, id)
    )

    conexion.commit()
    conexion.close()

    return redirect('/usuarios')

# =========================
# EJECUTAR SERVIDOR
# =========================

if __name__ == '__main__':
    app.run(debug=True, port=5001)

    # =========================
# AGREGAR PRODUCTO
# =========================

@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():

    try:

        producto = request.form.get('producto')
        cantidad = request.form.get('cantidad')

        # VALIDAR VACÍOS

        if not producto or not cantidad:
            return redirect('/inventario')

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

    except Exception as e:

        return f"ERROR: {e}"

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