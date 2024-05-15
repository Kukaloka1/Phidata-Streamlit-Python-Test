import streamlit as st
import logging
from dotenv import load_dotenv
import os
import requests

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
    from phi.assistant import Assistant
    from phi.tools.duckduckgo import DuckDuckGo
    assistant = Assistant(tools=[DuckDuckGo()], show_tool_calls=True)
    logger.debug("Asistente configurado correctamente.")
except Exception as e:
    logger.error(f"Error configurando el asistente: {e}")

# Función para obtener datos de Bitcoin desde CoinMarketCap
def get_bitcoin_data():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    headers = {
        'X-CMC_PRO_API_KEY': CMC_API_KEY
    }
    params = {
        'symbol': 'BTC',
        'convert': 'USD'
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error("Error al obtener datos de CoinMarketCap")
        return None

# Función para manejar la entrada del usuario
def handle_user_input(prompt):
    user_input = prompt
    logger.debug(f"Input del usuario: {user_input}")
    if user_input:
        # Añadir el mensaje del usuario al historial
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Obtener la respuesta del asistente
        try:
            if "precio de bitcoin" in user_input.lower():
                data = get_bitcoin_data()
                if data:
                    price = data['data']['BTC']['quote']['USD']['price']
                    response = f"El precio actual de Bitcoin es ${price}"
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    logger.debug(f"Respuesta del bot: {response}")
                else:
                    st.session_state.messages.append({"role": "assistant", "content": "Error al obtener el precio de Bitcoin."})
            else:
                response = ''.join(assistant.run(user_input))
                st.session_state.messages.append({"role": "assistant", "content": response})
                logger.debug(f"Respuesta del bot: {response}")
        except Exception as e:
            st.session_state.messages.append({"role": "assistant", "content": f"Error: {e}"})
            logger.error(f"Error obteniendo la respuesta del asistente: {e}")

        st.session_state.user_input = ""  # Limpiar el campo de entrada


