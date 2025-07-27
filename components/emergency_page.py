import streamlit as st
from geopy.geocoders import Nominatim
import urllib.parse
#from .sidebar import GLOBAL_RESOURCES
from components.shared_globals import GLOBAL_RESOURCES  # ✅ Corrected


def render_emergency_page():
    """Displays emergency help page with a dynamic Google search link."""

    if st.button("← Back to Chat", type="primary"):
        st.session_state.show_emergency_page = False
        # Clean up session state on exit
        st.session_state.pop('location_info', None)
        st.rerun()

    st.markdown("""
    <div class="main-header">
        <h1>Help is Available</h1>
        <div class="stAlert stInfo">If you are in immediate danger, please call your local emergency number (e.g., 911) immediately.</div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Find Local Resources Near You")
    geolocator = Nominatim(user_agent="talkheal_app")
    location_query = st.text_input(
        "Enter your City, State, or Country", placeholder="e.g., London, UK")

    if st.button("🔍 Search for Help", type="primary"):
        if location_query:
            with st.spinner(f"Searching for '{location_query}'..."):
                try:
                    location = geolocator.geocode(location_query)
                    if location:
                        # Store the essential location info
                        st.session_state.location_info = {
                            'lat': location.latitude,
                            'lon': location.longitude,
                            'name': location.address
                        }
                    else:
                        st.error(
                            f"Could not find a location for '{location_query}'. Please try again.")
                        st.session_state.pop('location_info', None)
                except Exception as e:
                    st.error(f"An error occurred during search: {e}")
                    st.session_state.pop('location_info', None)
        else:
            st.warning("Please enter a location to search.")

    # Display map and search link if a location has been found
    if 'location_info' in st.session_state:
        info = st.session_state.location_info
        lat, lon, name = info['lat'], info['lon'], info['name']

        st.success(f"Showing results for: {name}")

        # --- Map Display ---
        # Display a map centered on the user's searched location
        map_url = f"https://www.openstreetmap.org/export/embed.html?bbox={lon-0.1},{lat-0.1},{lon+0.1},{lat+0.1}&layer=mapnik&marker={lat},{lon}"
        st.components.v1.iframe(map_url, height=450)

        # --- Dynamic Google Search Link ---
        st.markdown("#### **Find Local Support**")
        st.info(
            "Click the button below for a comprehensive web search for support centers in your area.")

        search_term = f"mental health crisis support near {name}"
        encoded_search = urllib.parse.quote_plus(search_term)
        search_url = f"https://www.google.com/search?q={encoded_search}"

        st.markdown(
            f'<a href="{search_url}" target="_blank" class="emergency_button">🔍 Search Google for local crisis centers</a>', unsafe_allow_html=True)

    # --- Global Resources (Always available) ---
    with st.expander("View Global Crisis Hotlines", expanded=True):
        for resource in GLOBAL_RESOURCES:
            st.markdown(
                f"##### **{resource['name']}**: {resource['desc']} [Visit Website]({resource['url']})")
