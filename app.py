import streamlit as st
import google.generativeai as genai

# Configuração da página
st.set_page_config(page_title="Especialista Lexical", page_icon="💬", layout="centered")
st.title("💬 Especialista em Análise Lexical")
st.caption("Consulte, classifique e ajuste a análise de palavras de acordo com seu objetivo.")

# Autenticação com a API do Gemini
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Chave da API do Gemini não encontrada nos Secrets do Streamlit.")
    st.stop()

SYSTEM_PROMPT = """
Você é um Especialista em Análise Lexical e Consultor Linguístico Interativo.
Sua missão é guiar o usuário em um fluxo conversacional rigoroso, uma etapa por vez:

1. Faça uma saudação e pergunte qual é o objetivo dele.
2. Peça o contexto.
3. Solicite a palavra ou lista de palavras.
4. Faça a análise detalhada alinhada ao objetivo dele, e sugira categorias e pergunte se quer mudar as categorias ou criar novas.
5. Pergunte se deseja analisar novas palavras ou refinar.
Seja empático, didático e conduza uma etapa por turno de conversa.
"""

# Carrega o modelo com as instruções do sistema
@st.cache_resource
def load_model():
    return genai.GenerativeModel(
        model_name="gemini-1.5-pro",  # Ou "gemini-1.5-flash-002" / "gemini-1.5-pro"
        system_instruction=SYSTEM_PROMPT
    )

model = load_model()

# Inicializa o histórico do chat na sessão
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Exibe o histórico de mensagens
for message in st.session_state.chat.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Mensagem inicial do assistente (Etapa 1)
if len(st.session_state.chat.history) == 0:
    resposta_inicial = st.session_state.chat.send_message("Iniciar atendimento")
    with st.chat_message("assistant"):
        st.markdown(resposta_inicial.text)

# Entrada do usuário
if prompt := st.chat_input("Digite sua resposta aqui..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.spinner("O Especialista está digitando..."):
        resposta = st.session_state.chat.send_message(prompt)
        
    with st.chat_message("assistant"):
        st.markdown(resposta.text)
