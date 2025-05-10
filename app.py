import streamlit as st
from chatbot import get_chatbot_response
from state_manager import update_chat_state, extract_candidate_info
from config import initialize_session_state

initialize_session_state()

st.title("TalentScout Hiring Assistant")
st.subheader("Tech Recruitment Screening")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if len(st.session_state.messages) == 0:
    initial_greeting = """Hello! I'm the TalentScout Hiring Assistant. I'm here to help with the initial screening for tech positions. Could you please start by telling me your full name?"""
    with st.chat_message("assistant"):
        st.write(initial_greeting)
    st.session_state.messages.append({"role": "assistant", "content": initial_greeting})

if user_input := st.chat_input("Type your message here..."):
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    response = get_chatbot_response(user_input)
    with st.chat_message("assistant"):
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    extract_candidate_info(user_input, st.session_state.messages[-2]["content"])
    update_chat_state(user_input, response)

with st.sidebar:
    st.title("Debug Information")
    show_debug = st.checkbox("Show Debug Info")
    
    if show_debug:
        st.write("### Current State")
        st.write(st.session_state.chat_state)
        
        st.write("### Candidate Information")
        for key, value in st.session_state.candidate_info.items():
            st.write(f"**{key}:** {value}")
        
        if st.session_state.technical_questions:
            st.write("### Technical Questions")
            for i, question in enumerate(st.session_state.technical_questions):
                st.write(f"{i+1}. {question}")
            st.write(f"Current question index: {st.session_state.current_question_index}")
        
        if st.button("Reset Conversation"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.experimental_rerun()