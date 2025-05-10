import streamlit as st
import re
from question_generator import generate_technical_questions

def extract_candidate_info(user_input, bot_response):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_match = re.search(email_pattern, user_input)
    if email_match and not st.session_state.candidate_info["email"]:
        st.session_state.candidate_info["email"] = email_match.group()
    
    phone_pattern = r'\b(?:\+\d{1,3}[- ]?)?\(?\d{3}\)?[- ]?\d{3}[- ]?\d{4}\b'
    phone_match = re.search(phone_pattern, user_input)
    if phone_match and not st.session_state.candidate_info["phone"]:
        st.session_state.candidate_info["phone"] = phone_match.group()
    
    exp_pattern = r'\b(\d+)\s*(?:years?|yrs?)\b'
    exp_match = re.search(exp_pattern, user_input.lower())
    if exp_match and not st.session_state.candidate_info["experience"]:
        st.session_state.candidate_info["experience"] = exp_match.group(1) + " years"
    
    if "position" in bot_response.lower() and not st.session_state.candidate_info["position"]:
        st.session_state.candidate_info["position"] = user_input.strip()
    elif "location" in bot_response.lower() and not st.session_state.candidate_info["location"]:
        st.session_state.candidate_info["location"] = user_input.strip()
    elif "tech stack" in bot_response.lower() and not st.session_state.candidate_info["tech_stack"]:
        tech_input = user_input.strip()
        if tech_input:
            techs = [t.strip() for t in tech_input.split(',')]
            st.session_state.candidate_info["tech_stack"] = techs

def update_chat_state(user_input, bot_response):
    if st.session_state.exit_requested:
        st.session_state.chat_state = "ending"
        return
    
    current_state = st.session_state.chat_state
    
    if current_state == "greeting":
        if user_input.strip():
            st.session_state.candidate_info["name"] = user_input.strip()
            st.session_state.chat_state = "collecting_email"
    
    elif current_state == "collecting_email":
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.search(email_pattern, user_input):
            st.session_state.candidate_info["email"] = re.search(email_pattern, user_input).group()
            st.session_state.chat_state = "collecting_phone"
    
    elif current_state == "collecting_phone":
        phone_pattern = r'\b(?:\+\d{1,3}[- ]?)?\(?\d{3}\)?[- ]?\d{3}[- ]?\d{4}\b'
        if re.search(phone_pattern, user_input):
            st.session_state.candidate_info["phone"] = re.search(phone_pattern, user_input).group()
            st.session_state.chat_state = "collecting_experience"
        else:
            st.session_state.candidate_info["phone"] = user_input.strip()
            st.session_state.chat_state = "collecting_experience"
    
    elif current_state == "collecting_experience":
        st.session_state.candidate_info["experience"] = user_input.strip()
        st.session_state.chat_state = "collecting_position"
    
    elif current_state == "collecting_position":
        st.session_state.candidate_info["position"] = user_input.strip()
        st.session_state.chat_state = "collecting_location"
    
    elif current_state == "collecting_location":
        st.session_state.candidate_info["location"] = user_input.strip()
        st.session_state.chat_state = "collecting_tech_stack"
    
    elif current_state == "collecting_tech_stack":
        tech_input = user_input.strip()
        if tech_input:
            techs = [t.strip() for t in tech_input.split(',')]
            st.session_state.candidate_info["tech_stack"] = techs
            st.session_state.technical_questions = generate_technical_questions(techs)
            st.session_state.current_question_index = 0
            st.session_state.chat_state = "asking_technical_questions"
    
    elif current_state == "asking_technical_questions":
        st.session_state.current_question_index += 1
        if st.session_state.current_question_index >= len(st.session_state.technical_questions):
            st.session_state.chat_state = "ending"