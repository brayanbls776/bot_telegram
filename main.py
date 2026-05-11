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
        # Esto lee el contenido sin importar si es JSON perfecto o no
        body = await request.body()
        print(f"Contenido bruto recibido: {body.decode()}")
        
        data = await request.json()
        notificacion = data.get("texto", "No se pudo leer el texto")
        
        enviar_telegram(f"🔔 NUEVA NOTIFICACIÓN:\n{notificacion}")
        
    except Exception as e:
        # Si no es JSON, intentamos enviarlo como texto simple
        cuerpo_simple = await request.body()
        enviar_telegram(f"🔔 NOTIFICACIÓN (Texto plano):\n{cuerpo_simple.decode()}")
        print(f"Error procesando JSON, enviado como texto: {e}")

    return {"status": "recibido"}
