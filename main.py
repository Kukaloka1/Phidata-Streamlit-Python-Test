import streamlit as st
from assistant import handle_user_input  # Importa las funciones del asistente
from news_display import display_messages  # Importa la función de visualización de mensajes y noticias

# Título de la aplicación
st.title("BlockBodies.ai - Chat del Bot")

# Inicializa el estado de mensajes si no existe
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Configurar el input del usuario
prompt = st.chat_input("Escribe tu mensaje aquí...")

# Manejar la entrada del usuario
if prompt:
    handle_user_input(prompt)

# Mostrar la conversación y noticias
display_messages()













