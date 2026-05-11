from fastapi import FastAPI, Request
import requests
import os
app = FastAPI()

# --- CONFIGURACIÓN DE TELEGRAM ---
  # Añade esto arriba del todo


TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def enviar_telegram(mensaje):
    url = f"https://telegram.org{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje}
    requests.post(url, json=payload)

@app.get("/")
def home():
    return {"status": "Servidor de Yape Activo"}

@app.post("/yape")
async def recibir_yape(request: Request):
    data = await request.json()
    # El celular enviará el texto de la notificación
    notificacion = data.get("texto", "")
    
    print(f"Recibido: {notificacion}")
    
    # Reenviar a tu Telegram de inmediato
    enviar_telegram(f"🔔 NUEVA NOTIFICACIÓN:\n{notificacion}")
    
    return {"status": "recibido"}
