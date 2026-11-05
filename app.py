from flask import Flask, render_template, request

app = Flask(__name__)
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


@app.route("/rastreo")
def rastreo():
    return render_template("rastreo.html")

@app.route("/pedido", methods=["GET", "POST"])
def pedido():
    # Si el usuario le dio clic al botón Enviar...
    if request.method == "POST":
        # Atrapamos los datos usando los 'name' que indicamos en el HTML de pedido
        nombre_cliente = request.form.get("nme")
        correo_cliente = request.form.get("email")
        notas = request.form.get("especs")

        # Por ahora, solo lo imprimimos en la terminal de la computadora
        print(f"¡Llegó un pedido de {nombre_cliente}!")
        print(f"Correo: {correo_cliente}")
        print(f"Notas: {notas}")

        # Mostramos un mensaje temporal en el navegador
        return f"Gracias {nombre_cliente}, tu pedido fue recibido en el servidor."

    # Si el usuario solo está entrando a ver la página
    return render_template("pedido.html")

if __name__ == "__main__":
    app.run(debug=True)
