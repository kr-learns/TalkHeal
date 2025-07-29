import streamlit as st

# --- GLOBAL RESOURCES ---
GLOBAL_RESOURCES = {
    "Helplines": "https://www.who.int/teams/mental-health-and-substance-use/policy-law-rights/mental-health-in-emergencies",
    "Mental Health Resources": "https://www.mhanational.org/finding-help",
    "CBT Techniques": "https://www.therapistaid.com/therapy-guide/cbt"
}

# --- RENDER SIDEBAR FUNCTION ---
def render_sidebar():
    st.sidebar.markdown("""
        <style>
        .sidebar-title {
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("<div class='sidebar-title'>🧭 TalkHeal Navigation</div>", unsafe_allow_html=True)

    # Image
    st.sidebar.image("https://i.imgur.com/AdJ7lEf.jpeg", caption="Breathe. You're safe here.", use_container_width=True)

    # Chatbot tone selection
    TONE_OPTIONS = {
        "Compassionate Listener": "You are a compassionate listener — soft, empathetic, patient — like a therapist who listens without judgment.",
        "Motivating Coach": "You are a motivating coach — energetic, encouraging, and action-focused — helping the user push through rough days.",
        "Wise Friend": "You are a wise friend — thoughtful, poetic, and reflective — giving soulful responses and timeless advice.",
        "Neutral Therapist": "You are a neutral therapist — balanced, logical, and non-intrusive — asking guiding questions using CBT techniques.",
        "Mindfulness Guide": "You are a mindfulness guide — calm, slow, and grounding — focused on breathing, presence, and awareness."
    }

    selected_tone = st.sidebar.selectbox(
        "🎭 Select a personality tone:",
        options=list(TONE_OPTIONS.keys()),
        index=0,
        key="tone_selector"
    )
    st.session_state.selected_tone = selected_tone

    # Music player
    with st.sidebar.expander("🎵 Calm Background Music"):
        st.audio(
            "https://p.scdn.co/mp3-preview/26419f3cb70684b8798e0583c3e122ed2012dc17?cid=774b29d4f13844c495f206cafdad9c86",
            format="audio/mp3",
            start_time=0,
            use_container_width=True
        )

    # Expandable Sections
    with st.sidebar.expander("🧠 Mental Health Check"):
        st.markdown("Explore self-assessment tools to reflect on your mental wellbeing.")

    with st.sidebar.expander("📚 Resources & Knowledge Base"):
        for name, url in GLOBAL_RESOURCES.items():
            st.markdown(f"- [{name}]({url})")

    with st.sidebar.expander("☎️ Crisis Support"):
        st.markdown("If you're in danger or need immediate help, contact a local crisis line.")

    with st.sidebar.expander("🎨 Theme Settings"):
        st.markdown("Customize your experience with different themes (coming soon).")

    with st.sidebar.expander("🧪 Take PsyToolkit Verified Quizzes"):
        st.markdown("Gain insights into your psychological patterns using research-based tools.")

    # About Section
    st.sidebar.markdown("---")
    with st.sidebar.expander("ℹ️ About TalkHeal"):
        st.markdown("Your compassionate mental wellness companion, powered by AI and human empathy.")
