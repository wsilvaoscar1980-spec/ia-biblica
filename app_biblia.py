import streamlit as st
from google import genai

# 1. Configuração da Página Web
st.set_page_config(page_title="Mentor Teológico IA", page_icon="📖", layout="centered")
st.title("📖 Mentor Teológico - IA Bíblica")
st.write("Estudo profundo: Exegese, Hermenêutica, Apostasia, Apologética e Escatologia.")

# 2. Gerenciamento da Chave API (Insira na barra lateral)
with st.sidebar:
    st.header("Configuração")
    # api_key = st.text_input("Insira sua Gemini API Key:", type="password")
    st.markdown("[Obtenha uma chave gratuita aqui](https://aistudio.google.com/)")
    
    st.markdown("---")
    st.markdown("**Foco da Análise:**")
    foco = st.selectbox("Escolha uma linha de interpretação predominante:", 
                        ["Acadêmica/Ecumênica", "Histórica/Reformada", "Arminiana/Wesleyana", "Dispensacionalista"])

# 3. Inicializar o Histórico de Chat na memória do navegador
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir mensagens anteriores do chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. O Prompt de Sistema (As diretrizes teológicas rígidas da IA)
instrucoes_sistema = f"""
Você é um scholar teológico sênior de nível de doutorado, especialista em Exegese Bíblica, Hermenêutica, Apologética e Escatologia.
Seu objetivo é responder com o máximo de rigor acadêmico, utilizando o conhecimento de léxicos (como o Strong), variantes textuais, contexto histórico-cultural e os principais comentários teológicos da história.

Linha de interpretação solicitada pelo usuário: {foco}.

Sempre que o usuário enviar um versículo ou tema, estruture sua resposta com:
1. 🔍 **Análise Exegética & Textual:** Termos originais (Grego/Hebraico), nuances de tradução e semântica.
2. 🏛️ **Contexto Histórico-Cultural:** Quem escreveu, para quem, quando e por que o ambiente da época importa.
3. ⛓️ **Correlação Hermenêutica:** Como este trecho se conecta com a teologia bíblica progressiva (Antigo vs. Novo Testamento).
4. 🛡️ **Implicações (Apologéticas/Escatológicas):** Defesa de objeções comuns ou visões escatológicas associadas, conforme a linha selecionada.
"""

# 5. Fluxo do Chat
if pergunta := st.chat_input("Digite sua dúvida teológica (Ex: Analise Romanos 9 ou Explique o Milênio)..."):
    
    # Exibe a pergunta do usuário na tela
    with st.chat_message("user"):
        st.markdown(pergunta)
    st.session_state.messages.append({"role": "user", "content": pergunta})

    # Verifica se a chave API foi preenchida
    # Processamento da resposta da IA
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
        try:
        # Inicializa o cliente oficial do Google GenAI
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
                
                # Formata o histórico para o modelo
                historico_modelo = []
                for m in st.session_state.messages:
                    role_modelo = "user" if m["role"] == "user" else "model"
                    historico_modelo.append(types.Content(
                        role=role_modelo,
                        parts=[types.Part.from_text(text=m["content"])]
                    ))

                # Chama o modelo gratuito mais recente e rápido (Gemini 2.5 Flash / 1.5 Flash)
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=historico_modelo,
                    config=types.GenerateContentConfig(
                        system_instruction=instrucoes_sistema,
                        temperature=0.2, # Baixa criatividade para evitar heresias ou invenções
                    )
                )
                
                resposta_ia = response.text
                message_placeholder.markdown(resposta_ia)
                st.session_state.messages.append({"role": "assistant", "content": resposta_ia})
                
            except Exception as e:
                st.error(f"Erro ao chamar a API: {e}")
