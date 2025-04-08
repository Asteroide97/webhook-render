from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Número de WhatsApp autorizado (cambia si lo necesitas)
NUMEROS_AUTORIZADOS = ["whatsapp:+528715193928"]

# Carga la IP de tu PC desde una variable de entorno
TAILSCALE_PC_URL = os.getenv("LOCAL_SQL_ENDPOINT", "")

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    data = request.form
    mensaje = data.get("Body", "").strip()
    remitente = data.get("From", "").strip()

    print(f"📩 Mensaje recibido: {mensaje} de {remitente}")

    if remitente not in NUMEROS_AUTORIZADOS:
        print("❌ Número no autorizado:", remitente)
        return "Número no autorizado", 403

    if ":" not in mensaje:
        print("⚠️ Formato incorrecto:", mensaje)
        return "Formato incorrecto. Usa: L1:550", 400

    codigo, cantidad = mensaje.split(":", 1)
    codigo = codigo.upper().strip()
    cantidad = cantidad.strip()

    try:
        response = requests.post(TAILSCALE_PC_URL, json={
            "codigo": codigo,
            "cantidad": cantidad
        })
        print("✅ Petición enviada a local:", response.text)
        return f"Petición enviada: {codigo} - {cantidad}", response.status_code
    except Exception as e:
        print("🚫 Error al conectar con servidor local:", str(e))
        return f"Error al conectar con servidor local: {str(e)}", 500
