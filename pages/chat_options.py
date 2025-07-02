import streamlit as st
import json


st.title("Chat Options")

# Initialize session state for memory choice if it doesn't exist
if "memory_choice" not in st.session_state:
    st.session_state.memory_choice = True

st.header("Memory Settings")

# This checkbox controls the 'memory_choice' session state variable.
# This state is used by the chat_page to decide whether to include chat history.
st.session_state.memory_choice = st.checkbox(
    "Enable Memory (allows the bot to remember previous messages)",
    value=st.session_state.memory_choice,
)
st.metric(
    label="Total Messages in Current Session",
    value=len(st.session_state.get("messages", [])),
)

st.divider()

# Export Options
st.header("Export Chat")
if st.session_state.get("messages"):
    # Create a markdown string from the chat history
    chat_export_md = ""
    for msg in st.session_state.messages:
        chat_export_md += f"**{msg['role'].title()}**: {msg['content']}\n\n"
    st.download_button(
        "Download as Markdown (.md)",
        chat_export_md,
        "chat_history.md",
        "text/markdown",
    )

    # Create a JSON string from the chat history
    chat_export_json = json.dumps(st.session_state.messages, indent=2)
    st.download_button(
        "Download as JSON (.json)",
        chat_export_json,
        "chat_history.json",
        "application/json",
    )
else:
    st.caption("No messages to export yet. Start a conversation first!")
