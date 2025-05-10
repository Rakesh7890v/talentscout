import streamlit as st
import google.generativeai as genai

def get_chatbot_response(user_input):
    exit_keywords = ["goodbye", "exit", "quit", "bye", "end"]
    if any(keyword in user_input.lower() for keyword in exit_keywords):
        st.session_state.exit_requested = True
        return "Thank you for your time! We will review your application and get back to you soon. Have a great day!"
    
    candidate_info_formatted = "\n".join([
        f"- Name: {st.session_state.candidate_info['name']}",
        f"- Email: {st.session_state.candidate_info['email']}",
        f"- Phone: {st.session_state.candidate_info['phone']}",
        f"- Experience: {st.session_state.candidate_info['experience']}",
        f"- Position: {st.session_state.candidate_info['position']}",
        f"- Location: {st.session_state.candidate_info['location']}",
        f"- Tech Stack: {', '.join(st.session_state.candidate_info['tech_stack']) if st.session_state.candidate_info['tech_stack'] else 'Not provided'}"
    ])
    
    system_message = f"""
    You are TalentScout's AI Hiring Assistant. Your role is to screen candidates for tech positions.
    Follow these guidelines:
    1. Be professional, friendly, and concise with responses under 3 sentences when asking for information
    2. Gather the required information from candidates
    3. Ask only one question at a time
    4. Stay on topic of the hiring process
    
    Current information gathered:
    {candidate_info_formatted}
    
    Current state of the conversation: {st.session_state.chat_state}
    
    Your task based on the current state:
    - greeting: Introduce yourself briefly and ask for the candidate's name only
    - collecting_email: Ask for their email address only
    - collecting_phone: Ask for their phone number only
    - collecting_experience: Ask for their years of experience in their field
    - collecting_position: Ask what position they're applying for
    - collecting_location: Ask for their current location
    - collecting_tech_stack: Ask about their tech stack (programming languages, frameworks, etc.)
    - asking_technical_questions: Ask the next technical question from the list
    - ending: Thank them for their time and explain that TalentScout will review their application and contact them soon
    
    Keep your response concise and focused on the current state. Do not ask for multiple pieces of information at once.
    """
    
    if st.session_state.chat_state == "asking_technical_questions" and st.session_state.technical_questions:
        if st.session_state.current_question_index < len(st.session_state.technical_questions):
            current_question = st.session_state.technical_questions[st.session_state.current_question_index]
            system_message += f"\n\nCurrent technical question to ask: {current_question}"
    
    chat_history = []
    for message in st.session_state.messages:
        if message["role"] == "user":
            chat_history.append({"role": "user", "parts": [message["content"]]})
        else:
            chat_history.append({"role": "model", "parts": [message["content"]]})
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    chat = model.start_chat(history=chat_history)
    response = chat.send_message(f"{system_message}\n\nUser input: {user_input}")
    
    return response.text