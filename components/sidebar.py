import streamlit as st
from PIL import Image
import time

# --- GLOBAL EMERGENCY RESOURCES ---
GLOBAL_RESOURCES = {
    "India": {
        "Mental Health Helpline": "9152987821",
        "iCall": "9152987821",
        "Vandrevala Foundation": "1860 266 2345 / 9999 666 555"
    },
    "USA": {
        "National Suicide Prevention Lifeline": "1-800-273-TALK (8255)",
        "Crisis Text Line": "Text HOME to 741741"
    },
    "UK": {
        "Samaritans": "116 123",
        "Mind Helpline": "0300 123 3393"
    }
    # Add more countries and resources as needed
}

# --- NATURE IMAGE SLIDESHOW (For Music Player Visuals) ---
NATURE_IMAGES = [
    "https://images.unsplash.com/photo-1506744038136-46273834b3fb",
    "https://images.unsplash.com/photo-1496483648148-47c686dc86a8",
    "https://images.unsplash.com/photo-1507525428034-b723cf961d3e"
]

def render_sidebar():
    with st.sidebar:
        st.title("🌿 TalkHeal")

        # --- TONE SELECTION ---
       # st.header("🧠 Choose Your AI Tone")
       # selected_tone = st.selectbox(
           # "Select a personality tone:",
           # options=[
               # "Compassionate Listener",
               # "Motivating Coach",
               # "Wise Friend",
                #"Neutral Therapist",
               # "Mindfulness Guide"
           # ],
          #  index=0
     #   )
      #  st.session_state.selected_tone = selected_tone

        # --- SPOTIFY MUSIC PLAYER ---
        st.markdown("---")
        st.subheader("🎵 Soothing Music")

        # Optional: Rotate images every few seconds (simple slideshow)
        img_index = int(time.time()) % len(NATURE_IMAGES)
        st.image(NATURE_IMAGES[img_index], use_column_width=True)

        st.markdown("""
            <iframe style="border-radius:12px" 
                    src="https://open.spotify.com/embed/playlist/6zCID88oNjNv9zx6puDHKj?utm_source=generator" 
                    width="100%" height="80" frameborder="0" 
                    allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
                    loading="lazy">
            </iframe>
        """, unsafe_allow_html=True)

        # --- EMERGENCY RESOURCES ---
        st.markdown("---")
        st.subheader("🚨 Emergency Help")
        country = st.selectbox("Select your country:", list(GLOBAL_RESOURCES.keys()))
        if country:
            for name, contact in GLOBAL_RESOURCES[country].items():
                st.write(f"**{name}:** {contact}")
