import streamlit as st
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions
from dotenv import load_dotenv
import os
import re

load_dotenv()


@st.cache_resource
def init_connection():
    """Initializes and caches the Supabase connection."""
    load_dotenv()
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    opts = ClientOptions().replace(
        auto_refresh_token=True,  # Enable auto-refresh for better UX
        persist_session=True,  # Persist session across refreshes
        flow_type="implicit",  # Faster than PKCE for simple apps
    )
    supabase: Client = create_client(supabase_url, supabase_key, options=opts)  # type: ignore
    return supabase


#  Cache the email validation regex
@st.cache_data
def get_email_pattern():
    """Cache the email validation pattern."""
    return re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


def is_valid_email(email):
    """Uses cached regex to validate email format."""
    pattern = get_email_pattern()
    return pattern.match(email) is not None


# Cache session check to avoid repeated API calls
@st.cache_data(ttl=300)  # Cache for 5 minutes
def _get_session_data():
    """Get current session data with caching."""
    try:
        supabase = init_connection()
        session = supabase.auth.get_session()
        if session and session.user:
            return session.user.email
        return None
    except Exception:
        return None


def check_existing_session():
    """Checks if there's an existing Supabase session and updates session state."""
    if "session_checked" not in st.session_state:
        email = _get_session_data()
        if email:
            st.session_state.user_email = email
            st.session_state.session_checked = True
            return True
        st.session_state.session_checked = True
    return bool(st.session_state.get("user_email"))


def sign_up(email, password):
    """Signs up a new user."""
    try:
        supabase = init_connection()
        user = supabase.auth.sign_up({"email": email, "password": password})
        # Clear session cache after signup
        _get_session_data.clear()
        return user
    except Exception as e:
        st.error(f"Registration failed: {e}")
        return None


def sign_in(email, password):
    """Signs in a user."""
    try:
        supabase = init_connection()
        user = supabase.auth.sign_in_with_password(
            {"email": email, "password": password}
        )
        # Clear session cache after login
        _get_session_data.clear()
        return user
    except Exception as e:
        st.error(f"Login failed: {e}")
        return None


def sign_out():
    """Signs out the current user."""
    supabase = init_connection()
    try:
        supabase.auth.sign_out()
        # Clear all relevant session state
        keys_to_remove = ["user_email", "session_checked"]
        for key in keys_to_remove:
            if key in st.session_state:
                del st.session_state[key]
        # Clear session cache
        _get_session_data.clear()
        st.rerun()
    except Exception as e:
        st.error(f"Logout failed: {e}")


def update_user(new_email, new_password):
    """Updates the user's email and password."""
    try:
        supabase = init_connection()
        user_attributes = {}
        if new_email:
            user_attributes["email"] = new_email
        if new_password:
            user_attributes["password"] = new_password
        user = supabase.auth.update_user(user_attributes)
        # Clear session cache after update
        _get_session_data.clear()
        return user
    except Exception as e:
        st.error(f"Update failed: {e}")
        return None


def app_authentication():
    """Displays a customized authentication UI and handles logic."""
    # Check for existing session first
    if check_existing_session():
        st.rerun()
        return

    st.title("🎌 Weeaboo-Buddy")
    st.caption("Please log in or sign up to continue")

    with st.form("auth_form", clear_on_submit=False):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        col1, col2 = st.columns(2)

        with col1:
            login_button = st.form_submit_button("Log In", use_container_width=True)
        with col2:
            signup_button = st.form_submit_button(
                "Sign Up", use_container_width=True, type="secondary"
            )

        if login_button:
            if not email or not password:
                st.error("Please enter both email and password.")
            elif not is_valid_email(email):
                st.error("Please enter a valid email address.")
            else:
                with st.spinner("Logging in..."):
                    user = sign_in(email, password)
                    if user and user.user:
                        st.session_state.user_email = user.user.email
                        st.session_state.session_checked = True
                        st.success(f"Welcome back, {email}!")
                        st.rerun()

        if signup_button:
            if not email or not password:
                st.error("Please enter both email and password.")
            elif not is_valid_email(email):
                st.error("Please enter a valid email address.")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long.")
            else:
                with st.spinner("Creating your account..."):
                    user = sign_up(email, password)
                    if user and user.user:
                        st.success(
                            "Registration successful! Please log in to continue."
                        )
