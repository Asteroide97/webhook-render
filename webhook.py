from flask import Flask, request
import requests

app = Flask(__name__)

NUMEROS_AUTORIZADOS = ["whatsapp:+528715193928"]  # <-- ¡Correcto!

TAILSCALE_PC_URL = "http://100.72.42.36:5001/ejecutar"  # <-- ¡Correcto! (si es tu IP actual de Tailscale)

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    data = request.form
    mensaje = data.get("Body", "").strip()
    remitente = data.get("From", "").strip()

    if remitente not in NUMEROS_AUTORIZADOS:
        return "Número no autorizado", 403

    if ":" not in mensaje:
        return "Formato incorrecto. Usa: L1:550", 400

    codigo, cantidad = mensaje.split(":", 1)
    codigo = codigo.upper().strip()
    cantidad = cantidad.strip()

    try:
        response = requests.post(TAILSCALE_PC_URL, json={
            "codigo": codigo,
            "cantidad": cantidad
        })
        return f"Petición enviada: {codigo} - {cantidad}", response.status_code
    except Exception as e:
        return f"Error al conectar con servidor local: {str(e)}", 500
