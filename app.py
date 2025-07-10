import streamlit as st
from src.app.authentication import app_authentication, check_existing_session
from src.app.themes import CUSTOM_THEMES

# Page config - only set once
st.set_page_config(
    page_title="Weeaboo Buddy",
    page_icon="🎌",
    initial_sidebar_state="collapsed",
    layout="wide",  # Faster rendering than wide
)


# --- Optimize Theme Application ---
@st.cache_data
def get_theme_config(theme_name):
    """Cache theme configurations."""
    if theme_name in CUSTOM_THEMES:
        return CUSTOM_THEMES[theme_name].copy()
    return None


def apply_theme():
    """Apply theme only when it changes."""
    if "theme" not in st.session_state:
        st.session_state.theme = "Streamlit Light"

    theme_name = st.session_state.theme

    # Only apply theme if it's different from last time
    if (
        "last_applied_theme" not in st.session_state
        or st.session_state.last_applied_theme != theme_name
    ):
        if theme_name == "Streamlit Light":
            st._config.set_option("theme.base", "light")
        elif theme_name == "Streamlit Dark":
            st._config.set_option("theme.base", "dark")
        else:
            theme_config = get_theme_config(theme_name)
            if theme_config:
                st._config.set_option("theme.base", theme_config.pop("base", "light"))
                for key, value in theme_config.items():
                    st._config.set_option(f"theme.{key}", value)

        st.session_state.last_applied_theme = theme_name


# Apply theme
apply_theme()


# --- Cached Page Definitions ---
@st.cache_data
def get_pages():
    """Cache page definitions."""
    return [
        st.Page("pages/chat.py", title="Chat", icon="💬"),
        st.Page("pages/chat_options.py", title="Chat Options", icon="⚙️"),
        st.Page("pages/account.py", title="Account", icon="👤"),
    ]


# --- Main App Logic ---
if check_existing_session():
    # User is authenticated, show main app
    pages = get_pages()
    pg = st.navigation(pages, position="top")
    pg.run()
else:
    # User is not authenticated, show login screen
    app_authentication()
