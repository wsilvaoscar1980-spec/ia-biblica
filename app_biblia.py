import streamlit as st
from google import genai

# Configuração da página do navegador
st.set_page_config(page_title="Mentor Teológico IA", page_icon="📖", layout="centered")

st.title("📖 Mentor Teológico - IA")
st.write("Bem-vindo ao seu ambiente de estudos teológicos avançados. Faça perguntas sobre exegese, hermenêutica ou história bíblica.")

# Criação do cliente da IA usando a chave segura dos Secrets
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# Inicializa o histórico de mensagens se não existir
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe as mensagens anteriores do histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Caixa de entrada para o usuário digitar a pergunta
if prompt := st.chat_input("Digite sua pergunta teológica aqui..."):
    # Exibe a mensagem do usuário no chat
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Adiciona a pergunta ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Chama a API do Gemini para gerar a resposta
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        # Exibe a resposta do assistente
        with st.chat_message("assistant"):
            st.markdown(response.text)
        
        # Adiciona a resposta ao histórico
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
    except Exception as e:
        st.error(f"Erro ao chamar a API: {e}")



               
