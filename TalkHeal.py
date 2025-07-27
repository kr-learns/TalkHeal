import streamlit as st
import time
import google.generativeai as genai

from core.utils import save_conversations, load_conversations, get_current_time, create_new_conversation
from core.config import configure_gemini, PAGE_CONFIG
from css.styles import apply_custom_css
from components.header import render_header
from components.sidebar import render_sidebar
from components.chat_interface import render_chat_interface, handle_chat_input
from components.emergency_page import render_emergency_page

# --- 1. INITIALIZE SESSION STATE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "conversations" not in st.session_state:
    st.session_state.conversations = load_conversations()
if "active_conversation" not in st.session_state:
    st.session_state.active_conversation = -1
if "show_emergency_page" not in st.session_state:
    st.session_state.show_emergency_page = False
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "expanded"
if "mental_disorders" not in st.session_state:
    st.session_state.mental_disorders = [
        "Depression & Mood Disorders", "Anxiety & Panic Disorders", "Bipolar Disorder",
        "PTSD & Trauma", "OCD & Related Disorders", "Eating Disorders",
        "Substance Use Disorders", "ADHD & Neurodevelopmental", "Personality Disorders",
        "Sleep Disorders"
    ]
if "selected_tone" not in st.session_state:
    st.session_state.selected_tone = "Compassionate Listener"

# --- 2. SET PAGE CONFIG ---
st.set_page_config(
    page_title=PAGE_CONFIG["page_title"],
    page_icon=PAGE_CONFIG["page_icon"],
    layout=PAGE_CONFIG["layout"],
    initial_sidebar_state=st.session_state.sidebar_state
)

# --- 3. APPLY STYLES & CONFIGURATIONS ---
apply_custom_css()
model = configure_gemini()

# --- 4. TONE OPTIONS ---
TONE_OPTIONS = {
    "Compassionate Listener": "You are a compassionate listener — soft, empathetic, patient — like a therapist who listens without judgment.",
    "Motivating Coach": "You are a motivating coach — energetic, encouraging, and action-focused — helping the user push through rough days.",
    "Wise Friend": "You are a wise friend — thoughtful, poetic, and reflective — giving soulful responses and timeless advice.",
    "Neutral Therapist": "You are a neutral therapist — balanced, logical, and non-intrusive — asking guiding questions using CBT techniques.",
    "Mindfulness Guide": "You are a mindfulness guide — calm, slow, and grounding — focused on breathing, presence, and awareness."
}

# --- 5. SIDEBAR WITH MUSIC AND TONE SELECTION ---
with st.sidebar:
    st.markdown("### 🎿 Soothing Music")

    nature_images = [
        "https://images.unsplash.com/photo-1506744038136-46273834b3fb",
        "https://images.unsplash.com/photo-1507525428034-b723cf961d3e",
        "https://images.unsplash.com/photo-1493246507139-91e8fad9978e",
        "https://images.unsplash.com/photo-1502082553048-f009c37129b9",
    ]
    img_index = int(time.time() / 5) % len(nature_images)
    st.image(nature_images[img_index], use_container_width=True, caption="")

    st.markdown(
        """
        <div style="margin-top:10px; border-radius: 12px; background: rgba(255,255,255,0.07); padding: 10px;">
            <iframe style="border-radius:12px"
            src="https://open.spotify.com/embed/playlist/6zCID88oNjNv9zx6puDHKj?utm_source=generator"
            width="100%" height="152" frameBorder="0" allowfullscreen=""
            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture‑in‑picture"
            loading="lazy"></iframe>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.header("🧠 Choose Your AI Tone")
    selected_tone = st.selectbox(
        "Select a personality tone:",
        options=list(TONE_OPTIONS.keys()),
        index=list(TONE_OPTIONS.keys()).index(st.session_state.selected_tone)
    )
    st.session_state.selected_tone = selected_tone

# --- 6. GET PROMPT FOR TONE ---
def get_tone_prompt():
    return TONE_OPTIONS.get(
        st.session_state.get("selected_tone", "Compassionate Listener"),
        TONE_OPTIONS["Compassionate Listener"]
    )

# --- 7. RENDER SIDEBAR ---
render_sidebar()

# --- 8. PAGE ROUTING ---
main_area = st.container()

if not st.session_state.conversations:
    saved_conversations = load_conversations()
    if saved_conversations:
        st.session_state.conversations = saved_conversations
        if st.session_state.active_conversation == -1:
            st.session_state.active_conversation = 0
    else:
        create_new_conversation()
        st.session_state.active_conversation = 0
    st.rerun()

# --- 9. RENDER MAIN CONTENT ---
if st.session_state.get("show_emergency_page"):
    with main_area:
        render_emergency_page()
else:
    with main_area:
        render_header()
        st.subheader(f"🕡️ Current Chatbot Tone: **{st.session_state['selected_tone']}**")
        render_chat_interface()
        handle_chat_input(model, system_prompt=get_tone_prompt())

# --- 10. SCROLL TO BOTTOM SCRIPT ---
st.markdown("""
<script>
    function scrollToBottom() {
        var chatContainer = document.querySelector('.chat-container');
        if (chatContainer) {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    }
    setTimeout(scrollToBottom, 100);
</script>
""", unsafe_allow_html=True)
