from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

NUMEROS_AUTORIZADOS = ["whatsapp:+528715193928"]
TAILSCALE_PC_URL = os.getenv("LOCAL_SQL_ENDPOINT", "")

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    data = request.form
    mensaje = data.get("Body", "").strip()
    remitente = data.get("From", "").strip()

    print(f"📩 Mensaje recibido: {mensaje} de {remitente}")

    if remitente not in NUMEROS_AUTORIZADOS:
        return "Número no autorizado", 403

    if ":" not in mensaje:
        return "Formato incorrecto. Usa: L1:550", 400

    codigo, cantidad = mensaje.split(":", 1)
    codigo = codigo.strip().upper()
    cantidad = cantidad.strip()

    try:
        response = requests.post(TAILSCALE_PC_URL, json={
            "codigo": codigo,
            "cantidad": cantidad
        })
        print("✅ Petición enviada al servidor local")
        return f"Enviado: {codigo} - {cantidad}", response.status_code
    except Exception as e:
        print("❌ Error al conectar con servidor local:", str(e))
        return "Error al conectar con servidor local", 500
