from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Número de WhatsApp autorizado
NUMEROS_AUTORIZADOS = ["whatsapp:+528715193928"]

# Carga IP de tu PC (Tailscale) desde variable de entorno
TAILSCALE_PC_URL = os.getenv("LOCAL_SQL_ENDPOINT", "")

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
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
        print("✅ Petición enviada al servidor local:", response.text)
        return jsonify({"status": "ok", "response": response.text}), 200
    except Exception as e:
        print("🚫 Error al conectar con servidor local:", str(e))
        return f"Error al conectar con servidor local: {str(e)}", 500

# Ruta de prueba opcional para debug
@app.route("/", methods=["GET"])
def home():
    return "Webhook activo en /whatsapp", 200
