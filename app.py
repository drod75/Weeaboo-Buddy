import streamlit as st
from src.app.authentication import app_authentication

# Page Setup
st.set_page_config(
    page_title="Weeaboo-Buddy",
    page_icon="🎌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Define the pages for the navigation
pages = [
    st.Page("pages/chat.py", title="Chat", icon="💬"),
    st.Page("pages/chat_options.py", title="Chat Options", icon="⚙️"),
    st.Page("pages/account.py", title="Account", icon="👤"),
]

# Initialize user session state if it doesn't exist
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# Authentication check
if not st.session_state.user_email:
    # If user is not logged in, display the authentication screen
    app_authentication()
else:
    # If user is logged in, display the navigation and the selected page
    pg = st.navigation(pages, position="top")
    pg.run()
