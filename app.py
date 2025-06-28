import streamlit as st
from src.app.authentication import app_authentication
from src.app.content import app_content

# Page Setup
st.set_page_config(page_title="Weeaboo-Buddy", page_icon="🎌", layout="wide")
st.title("🎌 Weeaboo-Buddy")

# Initialize user session state if it doesn't exist
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# Authentication check
if st.session_state.user_email:
    # If user is logged in, display the main chat interface
    app_content()
else:
    # If user is not logged in, display the authentication screen
    app_authentication()
