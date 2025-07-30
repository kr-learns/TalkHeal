import streamlit as st
import google.generativeai as genai
import json
import os
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="TalkHeal - Mental Health Companion",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
def load_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Variables */
    :root {
        --primary-color: #e879f9;
        --secondary-color: #f472b6;
        --background-gradient: linear-gradient(135deg, #fdf2f8 0%, #fce7f3 100%);
        --text-primary: #1f2937;
        --text-secondary: #6b7280;
        --white: #ffffff;
        --border-radius: 12px;
        --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    /* Main App Styling */
    .stApp {
        background: var(--background-gradient);
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #e879f9 0%, #f472b6 100%);
        padding: 1rem;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #e879f9 0%, #f472b6 100%);
        color: white;
    }
    
    /* Sidebar Section Styling */
    .sidebar-section {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: var(--border-radius);
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .section-title {
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Emergency Help Section */
    .emergency-help {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: var(--border-radius);
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .emergency-title {
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .country-selector {
        width: 100%;
        padding: 0.5rem;
        border-radius: 8px;
        border: none;
        background: rgba(255, 255, 255, 0.9);
        color: #1f2937;
        font-size: 1rem;
        margin-bottom: 1rem;
    }
    
    .helpline-item {
        background: rgba(255, 255, 255, 0.1);
        padding: 0.75rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid white;
    }
    
    .helpline-label {
        color: white;
        font-weight: 500;
        font-size: 0.9rem;
    }
    
    .helpline-number {
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        margin-top: 0.25rem;
    }
    
    /* About Section */
    .about-section {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        margin: 2rem 0 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
    }
    
    .about-title {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
        color: white;
    }
    
    .about-content {
        font-size: 0.85rem;
        line-height: 1.5;
        color: rgba(255, 255, 255, 0.9);
    }
    
    .about-features {
        margin: 0.75rem 0;
    }
    
    .about-features li {
        margin: 0.25rem 0;
        font-size: 0.8rem;
    }
    
    .about-footer {
        margin-top: 1rem;
        padding-top: 0.75rem;
        border-top: 1px solid rgba(255, 255, 255, 0.2);
        font-size: 0.75rem;
        text-align: center;
        font-style: italic;
    }
    
    .about-creator {
        font-size: 0.8rem;
        margin-top: 0.5rem;
        color: rgba(255, 255, 255, 0.8);
    }
    
    /* Quick Suggestions */
    .quick-suggestion {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        padding: 0.5rem;
        margin: 0.25rem 0;
        color: white;
        font-size: 0.85rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .quick-suggestion:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
    }
    
    /* Main Chat Area */
    .chat-container {
        background: var(--white);
        border-radius: var(--border-radius);
        padding: 2rem;
        margin: 1rem;
        box-shadow: var(--shadow-lg);
    }
    
    /* Message Styling */
    .user-message {
        background: linear-gradient(135deg, #e879f9, #f472b6);
        color: white;
        padding: 1rem;
        border-radius: var(--border-radius);
        margin: 0.5rem 0;
        margin-left: 20%;
    }
    
    .assistant-message {
        background: #f8fafc;
        color: var(--text-primary);
        padding: 1rem;
        border-radius: var(--border-radius);
        margin: 0.5rem 0;
        margin-right: 20%;
        border-left: 4px solid var(--primary-color);
    }
    
    /* Mood Slider */
    .mood-container {
        text-align: center;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    .mood-emoji {
        font-size: 2rem;
        margin: 0.5rem;
    }
    
    /* Hide Streamlit Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .user-message, .assistant-message {
            margin-left: 0;
            margin-right: 0;
        }
        
        .chat-container {
            margin: 0.5rem;
            padding: 1rem;
        }
        
        .about-section {
            padding: 1rem;
            margin: 1rem 0;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Emergency helplines data
HELPLINES = {
    "India": {
        "Mental Health Helpline": "9152987821",
        "iCall": "9152987821", 
        "Vandrevala Foundation": "1860 266 2345 / 9999 666 555"
    },
    "United States": {
        "National Suicide Prevention Lifeline": "988",
        "Crisis Text Line": "Text HOME to 741741",
        "SAMHSA National Helpline": "1-800-662-4357"
    },
    "United Kingdom": {
        "Samaritans": "116 123",
        "Crisis Text Line": "Text SHOUT to 85258",
        "Mind Infoline": "0300 123 3393"
    },
    "Canada": {
        "Talk Suicide Canada": "1-833-456-4566",
        "Kids Help Phone": "1-800-668-6868",
        "Crisis Services Canada": "1-833-456-4566"
    },
    "Australia": {
        "Lifeline": "13 11 14",
        "Beyond Blue": "1300 22 4636",
        "Kids Helpline": "1800 55 1800"
    }
}

# AI Personality/Tone options
AI_PERSONALITIES = {
    "Compassionate Friend": {
        "description": "Warm, understanding, and supportive like a close friend",
        "prompt": "You are a compassionate friend who listens with empathy and offers gentle support. Use warm, understanding language and show genuine care for the person's wellbeing."
    },
    "Professional Counselor": {
        "description": "Professional, structured, and solution-focused",
        "prompt": "You are a professional mental health counselor. Provide structured, evidence-based guidance while maintaining professional boundaries. Offer practical strategies and techniques."
    },
    "Mindful Guide": {
        "description": "Calm, peaceful, and focused on mindfulness practices",
        "prompt": "You are a mindful guide who helps people find inner peace and awareness. Focus on breathing techniques, mindfulness practices, and present-moment awareness."
    },
    "Motivational Coach": {
        "description": "Encouraging, energetic, and goal-oriented",
        "prompt": "You are a motivational coach who inspires and energizes. Help people build confidence, set goals, and overcome challenges with enthusiasm and practical action steps."
    },
    "Gentle Listener": {
        "description": "Patient, quiet presence that validates and reflects",
        "prompt": "You are a gentle listener who provides a safe space for expression. Focus on validation, reflection, and helping people process their thoughts and feelings."
    }
}

# Mood tracking
MOODS = {
    1: {"emoji": "😢", "label": "Very Sad", "color": "#3b82f6"},
    2: {"emoji": "😔", "label": "Sad", "color": "#6366f1"},
    3: {"emoji": "😐", "label": "Neutral", "color": "#8b5cf6"},
    4: {"emoji": "🙂", "label": "Happy", "color": "#a855f7"},
    5: {"emoji": "😊", "label": "Very Happy", "color": "#c084fc"}
}

# Quick suggestions
QUICK_SUGGESTIONS = [
    "I'm feeling overwhelmed",
    "How to manage stress?",
    "I need someone to talk to",
    "Dealing with anxiety",
    "Feeling lonely lately",
    "Work-life balance tips",
    "Sleep problems",
    "Relationship issues",
    "Building self-confidence",
    "Coping with change"
]

# Mental health resources
RESOURCES = {
    "Coping Strategies": [
        "Deep breathing exercises",
        "Progressive muscle relaxation",
        "Mindfulness meditation",
        "Grounding techniques (5-4-3-2-1)",
        "Journaling prompts",
        "Physical exercise routines"
    ],
    "Professional Help": [
        "How to find a therapist",
        "Types of therapy explained",
        "Preparing for your first session",
        "Online therapy platforms",
        "Support groups near you",
        "Insurance and therapy costs"
    ],
    "Self-Care": [
        "Daily self-care routines",
        "Stress management techniques",
        "Healthy sleep habits",
        "Nutrition for mental health",
        "Building social connections",
        "Setting healthy boundaries"
    ]
}

def initialize_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'api_key' not in st.session_state:
        st.session_state.api_key = None
    if 'model' not in st.session_state:
        st.session_state.model = None
    if 'ai_personality' not in st.session_state:
        st.session_state.ai_personality = "Compassionate Friend"
    if 'current_mood' not in st.session_state:
        st.session_state.current_mood = 3
    if 'journal_entries' not in st.session_state:
        st.session_state.journal_entries = []
    if 'conversation_threads' not in st.session_state:
        st.session_state.conversation_threads = {"Default": []}
    if 'current_thread' not in st.session_state:
        st.session_state.current_thread = "Default"

def configure_ai():
    """Configure the Gemini AI model"""
    try:
        # Try to get API key from Streamlit secrets
        api_key = st.secrets.get("gemini", {}).get("api_key")
        if not api_key:
            # Fallback to environment variable
            api_key = os.getenv("GEMINI_API_KEY")
        
        if api_key:
            genai.configure(api_key=api_key)
            st.session_state.api_key = api_key
            st.session_state.model = genai.GenerativeModel('gemini-pro')
            return True
        else:
            st.error("🔑 Gemini API key not found. Please configure it in Streamlit secrets or environment variables.")
            return False
    except Exception as e:
        st.error(f"❌ Error configuring AI: {str(e)}")
        return False

def create_sidebar():
    """Create the enhanced sidebar with all features"""
    with st.sidebar:
        st.markdown("# 💜 TalkHeal")
        
        # AI Personality Selector
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🎭 AI Personality</div>', unsafe_allow_html=True)
        
        selected_personality = st.selectbox(
            "",
            options=list(AI_PERSONALITIES.keys()),
            index=list(AI_PERSONALITIES.keys()).index(st.session_state.ai_personality),
            key="personality_selector",
            help="Choose how TalkHeal should interact with you"
        )
        
        if selected_personality != st.session_state.ai_personality:
            st.session_state.ai_personality = selected_personality
        
        st.markdown(f"*{AI_PERSONALITIES[selected_personality]['description']}*")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Mood Tracker
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🌈 Current Mood</div>', unsafe_allow_html=True)
        
        mood_value = st.slider(
            "",
            min_value=1,
            max_value=5,
            value=st.session_state.current_mood,
            key="mood_slider"
        )
        
        if mood_value != st.session_state.current_mood:
            st.session_state.current_mood = mood_value
        
        current_mood = MOODS[mood_value]
        st.markdown(f"""
        <div class="mood-container">
            <div class="mood-emoji">{current_mood['emoji']}</div>
            <div style="color: white; font-weight: 500;">{current_mood['label']}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick Suggestions
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">💡 Quick Start</div>', unsafe_allow_html=True)
        
        for suggestion in QUICK_SUGGESTIONS[:5]:  # Show first 5 suggestions
            if st.button(suggestion, key=f"quick_{suggestion}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": suggestion})
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Conversation Threads
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">💬 Conversations</div>', unsafe_allow_html=True)
        
        # Thread selector
        thread_names = list(st.session_state.conversation_threads.keys())
        selected_thread = st.selectbox(
            "Select conversation:",
            options=thread_names,
            index=thread_names.index(st.session_state.current_thread),
            key="thread_selector"
        )
        
        if selected_thread != st.session_state.current_thread:
            # Save current messages to current thread
            st.session_state.conversation_threads[st.session_state.current_thread] = st.session_state.messages.copy()
            # Load selected thread
            st.session_state.current_thread = selected_thread
            st.session_state.messages = st.session_state.conversation_threads[selected_thread].copy()
            st.rerun()
        
        # New thread button
        if st.button("🆕 New Conversation", use_container_width=True):
            # Save current messages
            st.session_state.conversation_threads[st.session_state.current_thread] = st.session_state.messages.copy()
            # Create new thread
            new_thread_name = f"Chat {len(st.session_state.conversation_threads) + 1}"
            st.session_state.conversation_threads[new_thread_name] = []
            st.session_state.current_thread = new_thread_name
            st.session_state.messages = []
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Journal Section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📝 Quick Journal</div>', unsafe_allow_html=True)
        
        journal_text = st.text_area(
            "What's on your mind?",
            placeholder="Write a quick reflection...",
            height=100,
            key="journal_input"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save", use_container_width=True):
                if journal_text.strip():
                    entry = {
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "mood": st.session_state.current_mood,
                        "content": journal_text.strip()
                    }
                    st.session_state.journal_entries.append(entry)
                    st.success("Journal entry saved!")
                    st.session_state.journal_input = ""
        
        with col2:
            if st.button("💬 Discuss", use_container_width=True):
                if journal_text.strip():
                    prompt = f"I wrote this in my journal: '{journal_text.strip()}'. Can you help me process these thoughts?"
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    st.session_state.journal_input = ""
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Emergency Help Section
        st.markdown("""
        <div class="emergency-help">
            <div class="emergency-title">
                🚨 Emergency Help
            </div>
            <p style="color: white; margin-bottom: 1rem; font-size: 0.9rem;">Select your country:</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Country Selection
        selected_country = st.selectbox(
            "",
            options=list(HELPLINES.keys()),
            index=0,  # Default to India
            key="country_selector"
        )
        
        # Display helplines for selected country
        if selected_country and selected_country in HELPLINES:
            st.markdown('<div class="emergency-help">', unsafe_allow_html=True)
            for service, number in HELPLINES[selected_country].items():
                st.markdown(f"""
                <div class="helpline-item">
                    <div class="helpline-label">{service}:</div>
                    <div class="helpline-number">{number}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # About TalkHeal Section
        st.markdown("""
        <div class="about-section">
            <div class="about-title">ℹ️ About TalkHeal</div>
            <div class="about-content">
                Your compassionate mental health companion, designed to provide:
                <div class="about-features">
                    • 24/7 emotional support<br>
                    • Resource guidance<br>
                    • Crisis intervention<br>
                    • Professional referrals
                </div>
                <strong>Remember:</strong> This is not a substitute for professional mental health care.
            </div>
            <div class="about-footer">
                <div class="about-creator">
                    <strong>Created with ❤️ by Eccentric Explorer</strong>
                </div>
                <div style="margin-top: 0.5rem;">
                    <em>"It's absolutely okay not to be okay :)"</em>
                </div>
                <div style="margin-top: 0.5rem; font-size: 0.7rem;">
                    📅 Enhanced Version - May 2025
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def get_ai_response(message):
    """Get response from Gemini AI with mental health context and personality"""
    try:
        if not st.session_state.model:
            return "I'm sorry, but I'm having trouble connecting right now. Please try again in a moment."
        
        # Get current personality
        personality = AI_PERSONALITIES[st.session_state.ai_personality]
        current_mood = MOODS[st.session_state.current_mood]
        
        # Mental health assistant prompt with personality
        system_prompt = f"""You are TalkHeal, an empathetic and supportive mental health companion. 

Current personality mode: {st.session_state.ai_personality}
Personality guidance: {personality['prompt']}

The user's current mood is: {current_mood['label']} {current_mood['emoji']}

Your role is to:
1. Provide emotional support and validation
2. Offer practical coping strategies and techniques
3. Share mental health resources and information
4. Encourage professional help when appropriate
5. Maintain a warm, non-judgmental, and hopeful tone
6. Adapt your communication style to the selected personality

Important guidelines:
- Never provide diagnosis or replace professional medical advice
- Always encourage seeking professional help for serious concerns
- Be compassionate and understanding
- Offer practical, evidence-based suggestions
- Maintain appropriate boundaries
- If someone expresses suicidal thoughts, immediately direct them to emergency services
- Consider the user's current mood in your response

Respond in a caring, supportive manner while being helpful and informative."""
        
        full_message = f"{system_prompt}\n\nUser: {message}"
        response = st.session_state.model.generate_content(full_message)
        return response.text
    except Exception as e:
        return f"I apologize, but I'm experiencing some technical difficulties. Please try again. If the problem persists, please consider reaching out to a mental health professional or crisis helpline."

def main():
    """Main application function"""
    load_css()
    initialize_session_state()
    
    # Configure AI
    ai_configured = configure_ai()
    
    # Create sidebar
    create_sidebar()
    
    # Main chat interface
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Welcome message
    if not st.session_state.messages:
        current_mood = MOODS[st.session_state.current_mood]
        st.markdown(f"""
        # Welcome to TalkHeal 💜
        
        I'm here to listen, support, and help you navigate your mental health journey. 
        I can see you're feeling **{current_mood['label']}** {current_mood['emoji']} right now, and that's completely okay.
        
        **I'm currently in {st.session_state.ai_personality} mode** - {AI_PERSONALITIES[st.session_state.ai_personality]['description']}
        
        **Some ways I can help:**
        - Provide emotional support and validation
        - Share coping strategies and techniques  
        - Discuss mental health resources
        - Help you process difficult emotions
        - Encourage healthy habits and self-care
        - Journal reflection and discussion
        
        **Remember:** I'm here to complement, not replace, professional mental health care. 
        If you're in crisis, please use the emergency contacts in the sidebar.
        
        ---
        
        *How are you feeling today? What would you like to talk about?*
        """)
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if ai_configured:
        if prompt := st.chat_input("Share what's on your mind..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("I'm listening and thinking..."):
                    response = get_ai_response(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
    else:
        st.warning("⚠️ AI assistant is not available. Please check the API configuration.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    ---
    <div style="text-align: center; color: #6b7280; font-size: 0.8rem; padding: 1rem;">
        💜 TalkHeal - Your Mental Health Companion | Remember: You're not alone in this journey
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
