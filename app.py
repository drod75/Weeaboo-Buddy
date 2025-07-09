import streamlit as st
from src.app.authentication import app_authentication, init_connection
from src.app.themes import CUSTOM_THEMES  # Import themes

st.set_page_config(
    page_title="Weeaboo Buddy", page_icon="🎌", initial_sidebar_state="collapsed"
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

# --- Session Management ---
def check_authentication():
    """Check if user is authenticated, either from session state or Supabase session."""
    if "user_email" not in st.session_state:
        st.session_state.user_email = None
    
    # If no user in session state, check Supabase session
    if not st.session_state.user_email:
        try:
            supabase = init_connection()
            session = supabase.auth.get_session()
            if session and session.user:
                st.session_state.user_email = session.user.email
                return True
        except Exception:
            pass
    
    return bool(st.session_state.user_email)

# --- Main App Logic ---
if check_authentication():
    # User is authenticated, show main app
    pages = [
        st.Page("pages/chat.py", title="Chat", icon="💬"),
        st.Page("pages/chat_options.py", title="Chat Options", icon="⚙️"),
        st.Page("pages/account.py", title="Account", icon="👤"),
    ]
    
    pg = st.navigation(pages, position="top")
    pg.run()
else:
    # User is not authenticated, show login screen
    app_authentication()
