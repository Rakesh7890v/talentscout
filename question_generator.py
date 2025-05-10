import re
import google.generativeai as genai

def generate_technical_questions(tech_stack):
    if not tech_stack:
        return []
        
    prompt = f"""
    Generate 5 technical interview questions for a candidate who is proficient in the following technologies:
    {', '.join(tech_stack)}
    
    The questions should:
    1. Be specific to each technology mentioned
    2. Test both fundamental knowledge and advanced concepts
    3. Include at least one scenario-based or problem-solving question
    4. Be clear and concise
    5. Be presented as a numbered list
    """
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    
    questions_text = response.text
    questions = []
    
    for line in questions_text.split('\n'):
        if re.match(r'^\d+\.', line.strip()):
            questions.append(line.strip())
    
    if len(questions) < 3:
        fallback_questions = []
        for tech in tech_stack[:5]:
            fallback_questions.append(f"1. Could you explain your experience with {tech} and any projects you've worked on using it?")
            fallback_questions.append(f"2. What are the key features of {tech} that you find most useful?")
            fallback_questions.append(f"3. Can you describe a challenging problem you solved using {tech}?")
        return fallback_questions[:5]
    
    return questions[:5]