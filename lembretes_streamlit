import streamlit as st
import json
from datetime import datetime
import time
import threading
import requests
import os

ARQUIVO_JSON = 'lembretes.json'

# Configuração do CallMeBot
NUMERO = os.getenv("NUMERO")
APIKEY = os.getenv("APIKEY")       # <-- Altere aqui!

# Salvar lembrete no arquivo
def salvar_lembrete(titulo, mensagem, data_hora):
    lembrete = {"titulo": titulo, "mensagem": mensagem, "data_hora": data_hora}
    try:
        with open(ARQUIVO_JSON, 'r') as f:
            lembretes = json.load(f)
    except FileNotFoundError:
        lembretes = []

    lembretes.append(lembrete)
    with open(ARQUIVO_JSON, 'w') as f:
        json.dump(lembretes, f, indent=2)

# Carregar lembretes
def carregar_lembretes():
    try:
        with open(ARQUIVO_JSON, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Enviar mensagem via CallMeBot
def enviar_mensagem_whatsapp(mensagem):
    url = f"https://api.callmebot.com/whatsapp.php?phone={NUMERO}&text={mensagem}&apikey={APIKEY}"
    try:
        response = requests.get(url)
        return response.status_code == 200
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
        return False

# Monitorar lembretes e enviar via WhatsApp
def monitorar_lembretes():
    enviados = set()
    while True:
        lembretes = carregar_lembretes()
        agora = datetime.now().strftime("%Y-%m-%d %H:%M")
        for lembrete in lembretes:
            if lembrete["data_hora"] == agora and lembrete["data_hora"] not in enviados:
                msg = f"📌 {lembrete['titulo']}\n🕒 {lembrete['data_hora']}\n💬 {lembrete['mensagem']}"
