import streamlit as st
from phi.assistant import Assistant
from phi.tools.duckduckgo import DuckDuckGo
import logging
from dotenv import load_dotenv
import os

# Configuración de logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener las claves de API desde las variables de entorno
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
CMC_API_KEY = os.getenv('CMC_API_KEY')

# Log de las variables de entorno cargadas
logger.debug(f"OPENAI_API_KEY: {OPENAI_API_KEY}")
logger.debug(f"CMC_API_KEY: {CMC_API_KEY}")

# Configurar el asistente con herramientas
try:
    assistant = Assistant(tools=[DuckDuckGo()], show_tool_calls=True)
    logger.debug("Asistente configurado correctamente.")
except Exception as e:
    logger.error(f"Error configurando el asistente: {e}")

# Título de la aplicación
st.title("BlockBodies.ai - Chat del Bot")

# CSS personalizado para estilo de chat
st.markdown("""
    <style>
    .user-message { color: white; }
    .bot-message { color: ffffff; }
    </style>
    """, unsafe_allow_html=True)

# Contenedor para la conversación
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Función para manejar la entrada del usuario
def handle_user_input():
    user_input = st.session_state.user_input
    logger.debug(f"Input del usuario: {user_input}")
    if user_input:
        # Añadir el mensaje del usuario al historial
        st.session_state.messages.append({"role": "user", "content": user_input})
        # Obtener la respuesta del asistente
        try:
            response = ''.join(assistant.run(user_input))
            st.session_state.messages.append({"role": "bot", "content": response})
            logger.debug(f"Respuesta del bot: {response}")
        except Exception as e:
            st.session_state.messages.append({"role": "bot", "content": f"Error: {e}"})
            logger.error(f"Error obteniendo la respuesta del asistente: {e}")
        st.session_state.user_input = ""  # Limpiar el campo de entrada

# Input del usuario
st.text_input("Escribe tu mensaje aquí...", key="user_input", on_change=handle_user_input)

# Mostrar la conversación
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"<div class='user-message'>Antonio: {message['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-message'>Bot:{message['content']}</div>", unsafe_allow_html=True)

# Log para verificar que la aplicación ha arrancado
logger.debug("Aplicación Streamlit arrancada.")








