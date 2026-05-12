from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

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

@app.route('/login')
def login():
    return render_template('login.html')

# =========================
# DASHBOARD
# =========================

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

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
    return render_template('inventario.html')

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