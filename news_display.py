import streamlit as st

# CSS personalizado para estilo de chat y noticias
st.markdown("""
    <style>
    .chat-message {
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
        display: flex;
        align-items: center;
    }
    .user-message {
        background-color: #DCF8C6;
        text-align: right;
        color: #333333;
        justify-content: flex-end;
    }
    .assistant-message {
        background-color: #F1F0F0;
        text-align: left;
        color: #333333;
        justify-content: flex-start;
    }
    .chat-icon {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        object-fit: cover;
        margin: 0 10px;
    }
    .chat-container {
        display: flex;
        align-items: center;
    }
    .news-item {
        background-color: #F1F0F0;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
    }
    .news-title {
        font-weight: bold;
        color: #1E90FF;
    }
    .news-image {
        width: 100%;
        max-width: 600px;
        border-radius: 10px;
        margin-top: 10px;
    }
    .news-description {
        color: #333333;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Función para mostrar la conversación y noticias
def display_messages():
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(message['content'])
                
        else:
            with st.chat_message("assistant"):
                st.markdown(message['content']) 
            if "- Running: duckduckgo_news" in message['content']:
                st.markdown(message['content'].replace('- Running: duckduckgo_news', ''), unsafe_allow_html=True)
            elif "http" in message['content']:
                st.markdown(f"""
                <div class="news-item">
                    <div class="news-description">
                        <a href="{message['content']}" class="news-title" target="_blank">{message['content']}</a>
                    </div>
                    <img src="https://placekitten.com/800/400" class="news-image">
                </div>
                """, unsafe_allow_html=True)


