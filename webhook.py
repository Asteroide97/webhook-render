from flask import Flask, request
import requests
import os

app = Flask(__name__)  # <- esto es fundamental

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    data = request.form
    mensaje = data.get("Body", "").strip()
    remitente = data.get("From", "").strip()

    print(f"📩 Mensaje recibido: {mensaje} de {remitente}")

    if remitente != "whatsapp:+528715193928":
        return "Número no autorizado", 403

    if ":" not in mensaje:
        return "Formato incorrecto. Usa: L1:550", 400

    codigo, cantidad = mensaje.split(":", 1)
    response = requests.post(
        os.getenv("LOCAL_SQL_ENDPOINT"),
        json={"codigo": codigo.strip().upper(), "cantidad": cantidad.strip()}
    )
    return f"Enviado: {codigo} - {cantidad}", response.status_code
