# lembretes_bot.py

import time
import json
from datetime import datetime
from plyer import notification

def carregar_lembretes():
    try:
        with open('lembretes.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def notificar(titulo, mensagem):
    notification.notify(
        title=titulo,
        message=mensagem,
        timeout=10
    )

print("⏳ Bot de lembretes iniciado...")
enviados = set()

while True:
    lembretes = carregar_lembretes()
    agora = datetime.now().strftime("%Y-%m-%d %H:%M")

    for lembrete in lembretes:
        if lembrete["data_hora"] == agora and lembrete["data_hora"] not in enviados:
            notificar(lembrete["titulo"], lembrete["mensagem"])
            print(f"🔔 Notificação enviada: {lembrete['titulo']}")
            enviados.add(lembrete["data_hora"])

    time.sleep(30)
