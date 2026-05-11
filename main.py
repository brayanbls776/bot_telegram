from fastapi import FastAPI, Request
import requests
import os
app = FastAPI()

# --- CONFIGURACIÓN DE TELEGRAM ---
  # Añade esto arriba del todo


TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def enviar_telegram(mensaje):
    # LA LÍNEA DE ABAJO ES LA QUE ESTABA MAL EN TU CÓDIGO
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    payload = {"chat_id": CHAT_ID, "text": mensaje}
    try:
        r = requests.post(url, json=payload)
        print(f"Respuesta de Telegram: {r.status_code}")
    except Exception as e:
        print(f"Error al conectar con Telegram: {e}")


@app.get("/")
def home():
    return {"status": "Servidor de Yape Activo"}

@app.post("/yape")
async def recibir_yape(request: Request):
    try:
        data = await request.json()
        print(f"Datos recibidos: {data}") # Esto te permite ver en los logs de Render qué está llegando
        
        # Intentamos obtener el texto de diferentes formas según la app que uses
        notificacion = data.get("texto") or data.get("text") or data.get("body") or "Mensaje sin contenido"
        
        # Enviar a Telegram
        enviar_telegram(f"🔔 NUEVA NOTIFICACIÓN YAPE:\n{notificacion}")
        
    except Exception as e:
        print(f"Error procesando datos: {e}")
        
    return {"status": "recibido jajaja"}

