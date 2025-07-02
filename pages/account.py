import streamlit as st
from src.app.authentication import sign_out, update_user


st.title("Account Information")

st.write(f"**Email:** {st.session_state.user_email}")

with st.expander("Update Account Information"):
    with st.form("update_form"):
        new_email = st.text_input("New Email (optional)")
        new_password = st.text_input("New Password (optional)", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")

        submitted = st.form_submit_button("Update")

        if submitted:
            if new_password and new_password != confirm_password:
                st.error("Passwords do not match.")
            else:
                update_user(new_email, new_password)
                st.success("Account updated successfully!")
                if new_email:
                    st.session_state.user_email = new_email

if st.button("Log Out"):
    sign_out()
