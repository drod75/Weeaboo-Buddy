import streamlit as st
from src.app.authentication import app_authentication
from src.app.themes import CUSTOM_THEMES  # Import themes

st.set_page_config(
    page_title="Weeaboo Buddy", page_icon="🤖", initial_sidebar_state="collapsed"
)

# --- Apply The Selected Theme ---
# This must be the first Streamlit command in your app.

# Set the default theme if not in session state
if "theme" not in st.session_state:
    st.session_state.theme = "Streamlit Light"

# Get the selected theme name from session state
theme_name = st.session_state.theme

# Logic to apply the correct theme
if theme_name == "Streamlit Light":
    # Use the default Streamlit light theme
    st._config.set_option("theme.base", "light")
elif theme_name == "Streamlit Dark":
    # Use the default Streamlit dark theme
    st._config.set_option("theme.base", "dark")
elif theme_name in CUSTOM_THEMES:
    # Apply the full custom theme from the dictionary
    theme_config = CUSTOM_THEMES[theme_name]
    # Set the base first
    st._config.set_option("theme.base", theme_config.pop("base", "light"))
    # Apply all other theme settings
    for key, value in theme_config.items():
        st._config.set_option(f"theme.{key}", value)

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
