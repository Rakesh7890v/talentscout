import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

def load_api_key():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("Please set the GEMINI_API_KEY environment variable.")
        st.stop()
    return api_key

def configure_genai():
    api_key = load_api_key()
    genai.configure(api_key=api_key)

def initialize_session_state():
    configure_genai()
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "chat_state" not in st.session_state:
        st.session_state.chat_state = "greeting"

    if "candidate_info" not in st.session_state:
        st.session_state.candidate_info = {
            "name": "",
            "email": "",
            "phone": "",
            "experience": "",
            "position": "",
            "location": "",
            "tech_stack": []
        }

    if "technical_questions" not in st.session_state:
        st.session_state.technical_questions = []

    if "current_question_index" not in st.session_state:
        st.session_state.current_question_index = 0

    if "exit_requested" not in st.session_state:
        st.session_state.exit_requested = False