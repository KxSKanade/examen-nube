from flask import Flask, render_template, request, redirect, url_for, jsonify
import psycopg2
import os

app = Flask(__name__, template_folder='templates')

# Configuración de la base de datos en Render
DB_HOST = os.environ.get('DB_HOST', 'dpg-d01qguruibrs73b2tkug-a.oregon-postgres.render.com')
DB_NAME = os.environ.get('DB_NAME', 'dbexamen_banf')
DB_USER = os.environ.get('DB_USER', 'kanade')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'kgkhdjZ0CPrHtu58zFX6weXIhUJnYEKq')


def conectar_db():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, sslmode='require'
        )
        return conn
    except psycopg2.Error as e:
        print("Error al conectar a la base de datos:", e)
        return None


def crear_persona(dni, nombre, apellido, direccion, telefono):
    conn = conectar_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO personas (dni, nombre, apellido, direccion, telefono) VALUES (%s, %s, %s, %s, %s)",
            (dni, nombre, apellido, direccion, telefono)
        )
        conn.commit()
        conn.close()


def obtener_registros():
    conn = conectar_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM personas ORDER BY apellido")
        registros = cursor.fetchall()
        conn.close()
        return registros
    return []


@app.route('/')
def index():
    mensaje = request.args.get('mensaje_confirmacion')
    return render_template('index.html', mensaje_confirmacion=mensaje)


@app.route('/registrar', methods=['POST'])
def registrar():
    dni = request.form['dni']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    crear_persona(dni, nombre, apellido, direccion, telefono)
    mensaje_confirmacion = "Registro Exitoso"
    return redirect(url_for('index', mensaje_confirmacion=mensaje_confirmacion))


@app.route('/administrar')
def administrar():
    registros = obtener_registros()
    print("Registros obtenidos:", registros) 
    return render_template('administrar.html', registros=registros)



@app.route('/eliminar/<string:dni>', methods=['POST'])
def eliminar_registro(dni):
    conn = conectar_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM personas WHERE dni = %s", (dni,))
        conn.commit()
        conn.close()
    return redirect(url_for('administrar'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)