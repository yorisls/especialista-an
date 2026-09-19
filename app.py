import streamlit as st
from google import genai
from google.genai import types

# Configuração da página
st.set_page_config(page_title="Especialista Lexical", page_icon="💬", layout="centered")
st.title("💬 Especialista em Análise Lexical")
st.caption("Consulte, classifique e ajuste a análise de palavras de acordo com seu objetivo.")

# 1. Recupera a chave da API dos Secrets do Streamlit
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    st.error("Chave da API do Gemini não encontrada nos Secrets do Streamlit.")
    st.stop()

# 2. Inicializa o cliente do Gemini
client = genai.Client(api_key=api_key)

SYSTEM_PROMPT = """
Você é um Especialista em Análise Lexical e Consultor Linguístico Interativo.
Sua missão é guiar o usuário em um fluxo conversacional rigoroso, uma etapa por vez:

1. Faça uma saudação e pergunte qual é o objetivo dele (ex: marketing, acadêmico, suporte, branding).
2. Peça o contexto de uso (público-alvo, canal, etc.).
3. Solicite a palavra ou lista de palavras para analisar.
4. Faça a análise detalhada alinhada ao objetivo e contexto. Sugira categorias de classificação e pergunte explicitamente se o usuário quer mudar as categorias sugeridas ou criar novas.
5. Pergunte se deseja analisar novas palavras ou refinar a análise existente.

Seja empático, didático e conduza uma etapa por turno de conversa.
"""

# 3. Inicializa a sessão de chat mantendo o histórico
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model="gemini-2.5-flash",  # Nome do modelo atualizado e ativo
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.7,
        )
    )

# 4. Exibe o histórico de mensagens na tela
for message in st.session_state.chat.get_history():
    role = "user" if message.role == "user" else "assistant"
    text_content = message.parts[0].text if message.parts else ""
    if text_content:
        with st.chat_message(role):
            st.markdown(text_content)

# Mensagem inicial do assistente para iniciar o atendimento (Etapa 1)
if len(st.session_state.chat.get_history()) == 0:
    resposta_inicial = st.session_state.chat.send_message("Iniciar atendimento")
    with st.chat_message("assistant"):
        st.markdown(resposta_inicial.text)

# 5. Entrada do usuário
if prompt := st.chat_input("Digite sua resposta aqui..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.spinner("O Especialista está digitando..."):
        resposta = st.session_state.chat.send_message(prompt)
        
    with st.chat_message("assistant"):
        st.markdown(resposta.text)
