import sqlite3
from flask import Flask, render_template, request
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

def inicializar_bd():
    # Esto crea el archivo clinica.db si no existe, o se conecta si ya existe
    conexion = sqlite3.connect("clinica.db")
    cursor = conexion.cursor()

    # Escribimos el SQL puro para crear la tabla
    # Nota que agregamos un 'estatus' para usarlo luego en la vista de rastreo
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        email TEXT,
        telefono TEXT,
        servicio TEXT,
        especificaciones TEXT,
        estatus TEXT DEFAULT 'Recibido'
        )
    ''')
    conexion.commit()
    conexion.close()

# Ejecutamos la función para que la base de datos nazca
inicializar_bd()

datos_laboratorio = {
    "laboratorio": "Laboratorio Dental Blanco",
    "lema": "Recibimos sus archivos digitales STL, OBJ, PLY",
    "formatos_digitales_aceptados": ["STL", "OBJ", "PLY"],
    "catalogo_servicios": [
        {
            "categoria": "PORCELANA LIBRE DE METAL",
            "articulos": [
                {"concepto": "u. Monolítica multicapa zr", "precio_mxn": 1900},
                {"concepto": "u. Zirconio cofia", "precio_mxn": 1600},
                {"concepto": "u. Disilicato E-max", "precio_mxn": 1400},
                {"concepto": "u. p/implante (metal porcelana)", "precio_mxn": 1100},
                {"concepto": "u. p/implante de zirconio", "precio_mxn": 1900},
            ],
        },
        {
            "categoria": "METAL PORCELANA",
            "articulos": [
                {"concepto": "Estratificación avanzada", "precio_mxn": 900},
                {"concepto": "Personalizada", "precio_mxn": 650},
            ],
        },
        {
            "categoria": "CERÓMEROS",
            "articulos": [
                {"concepto": "Incrustación signum", "precio_mxn": 500},
                {"concepto": "Corona total signum", "precio_mxn": 700},
                {"concepto": "Incrustación Adoro", "precio_mxn": 600},
                {"concepto": "Corona total Adoro", "precio_mxn": 800},
            ],
        },
        {
            "categoria": "P.P.R. METÁLICA",
            "articulos": [
                {
                    "concepto": "Removible dentaurum GM800 bilateral (+acrílicas)",
                    "precio_mxn": 1800,
                },
                {
                    "concepto": "Removible dentaurum GM800 unilateral (+acrílicas)",
                    "precio_mxn": 800,
                },
            ],
        },
        {
            "categoria": "FIJA METÁLICA",
            "articulos": [
                {"concepto": "Endoposte", "precio_mxn": 120},
                {"concepto": "Incrustación (cerámica, LD)", "precio_mxn": 300},
                {"concepto": "Corona total (cerámica, LD)", "precio_mxn": 400},
                {"concepto": "Corona veneer/porcelana", "precio_mxn": 500},
                {"concepto": "Jaquet acrílico provisional", "precio_mxn": 80},
                {"concepto": "Jaquet acrílico alta resistencia", "precio_mxn": 150},
            ],
        },
        {
            "categoria": "REMOVIBLES FLEXIBLES",
            "articulos": [
                {"concepto": "Flexible bilateral (partial flex)", "precio_mxn": 1600},
                {"concepto": "Flexible unilateral (partial flex)", "precio_mxn": 800},
                {"concepto": "Flexible bilateral (valplas)", "precio_mxn": 1600},
                {"concepto": "Flexible unilateral (valplas)", "precio_mxn": 800},
                {"concepto": "Flexible bilateral (i-flex Tcs)", "precio_mxn": 1600},
                {"concepto": "Flexible unilateral (i-flex Tcs)", "precio_mxn": 800},
                {"concepto": "Placa total (Naturally Tcs)", "precio_mxn": 2000},
            ],
        },
        {
            "categoria": "PROSTODONCIAS",
            "articulos": [
                {"concepto": "Dentadura total anatómico (Probase)", "precio_mxn": 1400},
                {"concepto": "Dentadura total anatómico (Nictone)", "precio_mxn": 1100},
                {"concepto": "Dentadura parcial (+retenedores)", "precio_mxn": 750},
                {"concepto": "Dentadura provisional 2 a 6 pzas.", "precio_mxn": 450},
                {"concepto": "Retenedor wipla", "precio_mxn": 80},
                {"concepto": "Retenedor vaciado", "precio_mxn": 120},
                {"concepto": "Refuerzo malla o barra cri-ni", "precio_mxn": 250},
                {"concepto": "Guarda oclusal acrílico", "precio_mxn": 400},
                {"concepto": "Reparación", "precio_mxn": 250},
                {"concepto": "Rebase de dentadura", "precio_mxn": 350},
            ],
        },
        {
            "categoria": "REMOVIBLES HÍBRIDOS",
            "articulos": [
                {"concepto": "Bilateral (Dentaurum + i-flex Tcs)", "precio_mxn": 2500},
                {"concepto": "Unilateral (Dentaurum + i-flex Tcs)", "precio_mxn": 1100},
            ],
        },
    ],
}

def enviar_correo_confirmacion(email_cliente, nombre, servicio, folio):
    remitente = "tbhorchata@gmail.com"
    password = "Shwapau+1797"

    #Creacion del correo
    msg = EmailMessage()
    msg['Subject'] = f"Confirmacion de Pedido LDB - Folio # {folio}"
    msg['From'] = remitente
    msg['To'] = email_cliente

    cuerpo = f"""
    Hola {nombre},

    Hemos recibido tu solicitud exitosamente.
    Servicio solicitado: {servicio}
    
    Tu número de guía / folio para rastrear el pedido es: {folio}
    
    Gracias por confiar en Laboratorio Dental Blanco.
    ARETÉ - Persigue la excelencia en todo lo que hagas.
    """
    msg.set_content(cuerpo)

    # Nos conectamos al servidor de Gmail para enviarlo
    try:
        # El puerto 465 es el estándar para conexiones seguras SSL
        servidor = smtplib.SMTP_SSL('smtp.gmail.com, 465')
        servidor.login(remitente, password)
        servidor.send_message(msg)
        servidor.quit()
        print(f"Correo de confirmación enviado a {email_cliente}")
    except Exception as e:
        print(f"Ocurrió un error al enviar el correo: {e}")

@app.route("/servicios")
def catalogo():
    # Le pasamos la variable al HTML dándole un nombre (ej. 'datos')
    return render_template("servicios.html", datos=datos_laboratorio)

@app.route("/")
def labbla():
    return render_template("index.html")


@app.route("/servicios")
def servicios():
    return render_template("servicios.html")


@app.route("/rastreo", methods=["GET", "POST"])
def rastreo():
    estado_pedido = None #Variable vacia por defecto
    if request.method == "POST":
        # 1. Atrapamos el número de guía que escribió el usuario
        guia = request.form.get("nGuia")

        # 2. Nos conectamos a la base de datos
        conexion = sqlite3.connect("clinica.db")
        cursor = conexion.cursor()

        # 3. Buscamos el registro en la tabla
        # Nota: La coma en (guia,) es obligatoria en Python cuando envías un solo valor
        cursor.execute("SELECT estatus FROM pedidos WHERE id = ?", (guia,))

        # 4. fetchone() nos devuelve una "tupla" (un paquete) con el resultado, o 'None' si no existe
        registro = cursor.fetchone()

        conexion.close()

        # 5. Si encontramos algo, sacamos el estatus (que está en la posición 0 del paquete)
        if registro:
            estado_pedido = registro[0]
        else:
            estado_pedido = "No se encontro ningun pedido con ese numero de guia."
        
    # Enviamos el HTML, pasándole la variable 'resultado'
    return render_template("rastreo.html", resultado=estado_pedido)

@app.route("/pedido", methods=["GET", "POST"])
def pedido():
    # Si el usuario le dio clic al botón Enviar...
    if request.method == "POST":
        # 1. Atrapamos los datos usando los 'name' que indicamos en el HTML de pedido
        nombre_cliente = request.form.get("nme")
        correo_cliente = request.form.get("email")
        telefono_cliente = request.form.get("tel")
        servicio_elegido = request.form.get("servicio")
        notas = request.form.get("especs")
        

        # 2. Nos conectamos a la base de datos
        conexion = sqlite3.connect("clinica.db")
        cursor = conexion.cursor()

        # 3. Ejecutamos el INSERT. 
        # IMPORTANTE: En SQLite usamos signos de interrogación (?) por seguridad para evitar Inyecciones SQL.
        cursor.execute(
            "INSERT INTO pedidos (nombre, email, telefono, servicio, especificaciones) VALUES (?, ?, ?, ?, ?)",
            (nombre_cliente, correo_cliente, telefono_cliente, servicio_elegido, notas)
        )

        # 4. Atrapamos el ID que la BD genero
        folio = cursor.lastrowid

        # 5. Guardamos los cambios y cerramos la conexión
        conexion.commit()
        conexion.close()

        enviar_correo_confirmacion(correo_cliente, nombre_cliente, servicio_elegido, folio)

        # Mostramos un mensaje temporal en el navegador
        return f"Gracias {nombre_cliente}, tu pedido fue recibido y se envio un correo a {correo_cliente} numero de guia es {folio}."

    # Si el usuario solo está entrando a ver la página
    return render_template("pedido.html", datos = datos_laboratorio)

if __name__ == "__main__":
    app.run(debug=True)
