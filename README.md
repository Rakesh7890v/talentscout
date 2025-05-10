# TalentScout Hiring Assistant

## Project Overview

TalentScout Hiring Assistant is an AI-powered chatbot designed to streamline the technical recruitment process. It conducts initial candidate screenings through a conversational interface, automatically gathering candidate information and assessing technical competencies.

**Key Features:**
- Interactive chat interface for natural conversations
- Structured interview flow for consistent candidate experiences
- Automatic collection of candidate data (contact info, experience, etc.)
- Dynamic generation of technical questions tailored to each candidate's skill set
- Real-time information extraction and state management

The assistant helps recruiters save time by handling routine screening tasks, allowing them to focus on evaluating higher-level candidate qualities.

## Installation Instructions

### Prerequisites
- Python 3.7+
- Google Cloud account with Gemini API access

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/rakesh7890v/talentscout.git
   cd talentscout
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   - Copy the `.env.example` file to create a new `.env` file
   ```bash
   cp .env.example .env
   ```
   - Edit the `.env` file and add your Gemini API key
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the application**
   - Open your browser and navigate to `http://localhost:8501`

## Usage Guide

### For Recruiters

1. **Start the application** using the installation instructions above.
2. The chatbot will automatically begin the interview process with candidates.
3. **Monitor the conversation** as the chatbot collects candidate information.
4. Use the **Debug panel** in the sidebar (toggle "Show Debug Info") to view:
   - Current conversation state
   - Collected candidate information
   - Generated technical questions
   - Current question progress
5. Use the **Reset Conversation** button to start over with a new candidate.

### Conversation Flow

The chatbot follows this structured interview process:
1. Welcome and collect candidate's name
2. Gather contact information (email, phone)
3. Collect professional details (experience, position, location)
4. Ask about technical skills and stack
5. Generate and ask tailored technical questions
6. Conclude the interview with next steps

## Technical Details

### Architecture

The application is built with a modular architecture:
- `app.py`: Main Streamlit application and UI
- `config.py`: Configuration and session state initialization
- `chatbot.py`: Response generation with Gemini
- `state_manager.py`: Conversation state machine and data extraction
- `question_generator.py`: Technical question generation

### Technologies Used

- **Streamlit**: Web application framework for the UI
- **Google Generative AI**: Powers the conversational AI (Gemini 1.5 Flash model)
- **Python-dotenv**: Environment variable management
- **Regular Expressions**: Information extraction from candidate responses

### Model Details

The application uses the **Gemini 1.5 Flash** model from Google, which provides:
- Natural conversational abilities
- Context-aware responses
- Ability to follow structured prompts
- Technical knowledge for generating relevant questions

## Prompt Design

The system employs a sophisticated prompt engineering approach:

### Main Chatbot Prompt

The primary system prompt includes:
- Role definition ("TalentScout's AI Hiring Assistant")
- Behavioral guidelines (professional, concise, focused)
- Current candidate information
- Conversation state
- Task instructions specific to the current state

This structured prompt ensures the model stays on track while maintaining a natural conversation flow.

### Technical Question Generation

For generating technical questions, a specialized prompt:
1. Specifies the candidate's tech stack
2. Defines question requirements (specific to technologies, testing fundamentals and advanced concepts)
3. Requests a specific format (numbered list)
4. Includes fallback mechanisms if generation fails

### State Management

The system maintains a state machine with these key states:
- `greeting`: Initial introduction
- `collecting_*`: Various stages of information collection
- `asking_technical_questions`: Technical assessment phase
- `ending`: Conclusion of interview

Each state transition has clear rules based on the presence of specific information in candidate responses.

## Challenges & Solutions

### Challenge 1: Information Extraction
**Problem**: Reliably extracting structured data from unstructured candidate responses.  
**Solution**: Implemented regex patterns for standard formats (email, phone numbers) and contextual extraction based on previous questions. This hybrid approach provides flexibility while maintaining accuracy.

### Challenge 2: Conversation Coherence
**Problem**: Maintaining a natural conversation flow while following a structured interview process.  
**Solution**: Designed a state machine with clear transitions and context preservation. The system only moves forward when required information is obtained, creating a natural conversation that still collects all necessary data.

### Challenge 3: Technical Question Quality
**Problem**: Generating relevant technical questions for diverse technology stacks.  
**Solution**: Leveraged Gemini's technical knowledge with carefully crafted prompts that specify question qualities. Added fallback mechanisms to ensure a minimum set of quality questions even when the model struggles with obscure technologies.

### Challenge 4: Handling Unexpected Inputs
**Problem**: Gracefully handling off-topic responses or partial information.  
**Solution**: Implemented information extraction that works with partial matches and a state machine that doesn't advance until required information is provided. The system can extract valuable information even from complex or tangential responses.

### Challenge 5: Debug Capabilities
**Problem**: Providing oversight for recruiters without disrupting the candidate experience.  
**Solution**: Created a separate debug sidebar that provides real-time insights into the conversation state and collected information without affecting the main chat interface.
