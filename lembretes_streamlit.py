import streamlit as st
import json
from datetime import datetime
import time
import threading
import requests
from dotenv import load_dotenv
load_dotenv()
import os
import io
import pytz

agora = datetime.now(pytz.timezone("America/Sao_Paulo")).strftime("%Y-%m-%d %H:%M")
ARQUIVO_JSON = 'lembretes.json'

# Configuração do CallMeBot
NUMERO = os.getenv("NUMERO")
APIKEY = os.getenv("APIKEY")       # <-- Altere aqui!
#GRUPO = os.getenv("GRUPO") 
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

def substituir_lembretes_novo_arquivo(novo_conteudo):
    try:
        dados = json.loads(novo_conteudo)
        print("DEBUG - JSON carregado:", dados)
        if isinstance(dados, list):
            with open(ARQUIVO_JSON, 'w') as f:
                json.dump(dados, f, indent=2)
            print("DEBUG - Dados escritos em", ARQUIVO_JSON)
            return True, "Lembretes carregados com sucesso!"
        else:
            return False, "Formato inválido: o JSON deve ser uma lista."
    except Exception as e:
        return False, f"Erro ao carregar JSON: {e}"
    
# Enviar mensagem via CallMeBot
def enviar_mensagem_whatsapp(mensagem):
    url = f"https://api.callmebot.com/whatsapp.php?phone={NUMERO}&text={mensagem}&apikey={APIKEY}"
    print(url)
    try:
        response = requests.get(url)
        return response.status_code == 200
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
        return False
    
def enviar_para_grupo(mensagem):
    url = f"https://api.callmebot.com/whatsapp.php?group={GRUPO}&text={mensagem}&apikey={APIKEY}"
    print(url)
    try:
        response = requests.get(url)
        return response.status_code == 200
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
        return False
    
def reset_checkbox():
    st.session_state.confirma_limpar = False

# Monitorar lembretes e enviar via WhatsApp
def monitorar_lembretes():
    enviados = set()  # controla lembretes já enviados para não repetir
    while True:
        lembretes = carregar_lembretes()
        agora = datetime.now(pytz.timezone("America/Sao_Paulo")).strftime("%Y-%m-%d %H:%M") # datetime.now().strftime("%Y-%m-%d %H:%M")

        for lembrete in lembretes:
            # Se o horário do lembrete é igual ao atual e ainda não foi enviado
            if lembrete["data_hora"] == agora and lembrete["data_hora"] + lembrete["titulo"] not in enviados:
                msg = f"📌 {lembrete['titulo']}\n🕒 {lembrete['data_hora']}\n💬 {lembrete['mensagem']}"
                sucesso = enviar_mensagem_whatsapp(msg)
                if sucesso:
                    enviados.add(lembrete["data_hora"] + lembrete["titulo"])
                    print(f"Lembrete enviado: {msg}")
                else:
                    print("Falha ao enviar lembrete")
                #sucesso_grupo = enviar_para_grupo(msg)
                #if sucesso_grupo:
                #    enviados.add(lembrete["data_hora"] + lembrete["titulo"])
                #    print(f"Lembrete enviado no grupo: {msg}")
                #else:
                #    print("Falha ao enviar lembrete no grupo")

        time.sleep(10)  # verifica a cada 30 segundos

# Rodar thread de monitoramento apenas uma vez
if 'monitorando' not in st.session_state:
    st.session_state.monitorando = True
    threading.Thread(target=monitorar_lembretes, daemon=True).start()

# --- Interface do App ---
st.title("📱 Lembretes via CallMeBot")

with st.form("form_lembrete"):
    titulo = st.text_input("Título do lembrete")
    mensagem = st.text_input("Mensagem")
    data = st.date_input("Data")
    hora = st.time_input("Hora")

    if st.form_submit_button("Adicionar lembrete"):
        data_hora = f"{data} {hora.strftime('%H:%M')}"
        salvar_lembrete(titulo, mensagem, data_hora)
        st.success("✅ Lembrete adicionado!")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🗑️ Limpar")
    if st.button("⚠️ Apagar lembretes"):
        try:
            with open(ARQUIVO_JSON, 'w') as f:
                json.dump([], f)
            st.success("✅ Todos os lembretes foram apagados.")
        except Exception as e:
            st.error(f"Erro ao apagar lembretes: {e}")

with col2:
    st.subheader("💾 Exportar")
    try:
        with open(ARQUIVO_JSON, 'r') as f:
            dados = f.read()
        buffer = io.BytesIO(dados.encode('utf-8'))
        st.download_button(
            label="📥 Baixar lembretes",
            data=buffer,
            file_name="lembretes.json",
            mime="application/json"
        )
    except FileNotFoundError:
        st.warning("Nenhum lembrete salvo ainda para exportar.")

with col3:
    st.subheader("⬆️ Importar")
    uploaded_file = st.file_uploader("Escolha o arquivo lembretes.json", type=["json"])
    if uploaded_file is not None:
        conteudo = uploaded_file.read().decode("utf-8")
        sucesso, msg = substituir_lembretes_novo_arquivo(conteudo)

        # Resetar os estados de exclusão
        st.session_state.confirmar_exclusao = False
        st.session_state.exclusao_realizada = False

        if sucesso:
            st.success(msg)
        else:
            st.error(msg)

st.subheader("📋 Lembretes agendados")
lembretes = carregar_lembretes()
if lembretes:
    for l in lembretes:
        st.markdown(f"- **{l['data_hora']}** — {l['mensagem']}")
else:
    st.info("Nenhum lembrete cadastrado ainda.")

