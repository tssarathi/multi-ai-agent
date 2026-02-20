import requests
import streamlit as st

from src.config.config import config
from src.utils.logger import get_logger

logger = get_logger(__name__)

st.set_page_config(page_title="Multi AI Agent", layout="centered", page_icon=":robot:")

st.title("Multi AI Agent")

system_prompt = st.text_area("Define your AI Agent: ", height=70)
selected_model = st.selectbox("Select a model", config.ALLOWED_MODELS)

allow_websearch = st.checkbox("Allow web search", value=True)

user_query = st.text_area("Enter your query: ", height=150)

API_URL = "http://127.0.0.1:8000/chat"

if st.button("Ask Agent") and user_query.strip():
    payload = {
        "llm_id": selected_model,
        "system_prompt": system_prompt,
        "allow_websearch": allow_websearch,
        "messages": user_query,
    }

    try:
        logger.info(f"Sending payload: {payload} to API")

        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            agent_response = response.json().get("response", "")

            logger.info(f"Successfully got response from API: {agent_response}")

            st.subheader("Agent Response")
            st.markdown(agent_response.replace("\n", "<br>"), unsafe_allow_html=True)

        else:
            logger.error(f"Failed to get response from API: {response.status_code}")
            st.error(f"Failed to get response from API: {response.status_code}")

    except Exception as e:
        logger.error(f"Error getting response from API: {e}")
        st.error(f"Error getting response from API: {e}")
