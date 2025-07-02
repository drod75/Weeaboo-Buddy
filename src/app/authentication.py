import streamlit as st
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions
from dotenv import load_dotenv
import os
import re


@st.cache_resource
def init_connection():
    """Initializes and caches the Supabase connection."""
    load_dotenv()
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    opts = ClientOptions().replace(auto_refresh_token=False)
    supabase: Client = create_client(supabase_url, supabase_key, options=opts)  # type: ignore
    return supabase


# --- Authentication Functions ---


def sign_up(email, password):
    """Signs up a new user."""
    try:
        supabase = init_connection()
        user = supabase.auth.sign_up({"email": email, "password": password})
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
        return user
    except Exception as e:
        st.error(f"Login failed: {e}")
        return None


def sign_out():
    """Signs out the current user."""
    supabase = init_connection()
    try:
        supabase.auth.sign_out()
        for key in st.session_state.keys():
            if key == "user_email":
                del st.session_state[key]
        st.rerun()
    except Exception as e:
        st.error(f"Logout failed: {e}")


def is_valid_email(email):
    """Uses regex to validate email format."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


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
        return user
    except Exception as e:
        st.error(f"Update failed: {e}")
        return None


# --- Main UI Function ---


def app_authentication():
    """Displays a customized authentication UI and handles logic."""
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
