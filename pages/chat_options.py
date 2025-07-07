import streamlit as st
import json
import os
from src.agent.agent import WeeabooBudddy
from src.app.themes import ALL_THEMES  # Import your presets

st.title("Chat Options")

# Initialize session state for memory choice if it doesn't exist
if "memory_choice" not in st.session_state:
    st.session_state.memory_choice = True


def cleanup_temp_files():
    """Clean up temporary files"""
    if "temp_files" in st.session_state:
        for temp_file in st.session_state.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
            except Exception as e:
                st.error(f"Error cleaning up temp file {temp_file}: {str(e)}")
        st.session_state.temp_files = []


def clear_thread_history():
    """Clear the user's thread history from LangGraph state/MongoDB"""
    try:
        # Get the agent instance
        agent = WeeabooBudddy()

        # Get the thread ID (user email)
        thread_id = st.session_state.get("user_email", "default")

        # Configure for the specific thread
        config = {"configurable": {"thread_id": thread_id}}

        # Get the current state to check if it exists
        current_state = agent.get_state(config)

        if current_state and hasattr(current_state, "values") and current_state.values:
            # Clear the state by updating it with empty messages
            agent.update_state(config, {"messages": []})
            st.success("Thread history cleared from database!")
            return True
        else:
            st.info("No thread history found in database to clear.")
            return True

    except Exception as e:
        st.error(f"Error clearing thread history: {str(e)}")
        return False


# This callback function runs immediately when the user makes a selection
def update_theme():
    # The value from the selectbox is automatically stored in its key
    st.session_state.theme = st.session_state.theme_selector
    # Explicitly trigger a rerun to ensure the app updates.
    st.rerun()


# Set a default theme if one doesn't exist in the session state
if "theme" not in st.session_state:
    st.session_state.theme = "Streamlit Light"

# The selectbox now uses a `key` and an `on_change` callback
st.selectbox(
    label="Choose a Theme",
    options=ALL_THEMES,
    key="theme_selector",  # The key to access the widget's state
    on_change=update_theme,  # The function to call when the value changes
    index=ALL_THEMES.index(st.session_state.theme),  # Set default value
)

st.info("You can add up to 20 different themes for users to choose from!")

st.header("Memory Settings")

# This checkbox controls the 'memory_choice' session state variable.
# This state is used by the chat_page to decide whether to include chat history.
st.metric(
    label="Total Messages in Current Session",
    value=len(st.session_state.get("messages", [])),
)

st.divider()

# Temporary Files Management
st.header("File Management")

# Show number of temporary files
temp_files_count = len(st.session_state.get("temp_files", []))
st.metric(
    label="Temporary Image Files",
    value=temp_files_count,
    help="Images uploaded during the chat session are stored as temporary files",
)

# Clean up temp files button
if temp_files_count > 0:
    if st.button("🗑️ Clean up temporary files", type="secondary"):
        cleanup_temp_files()
        st.success("Temporary files cleaned up!")
        st.rerun()

    # Show file details in an expander
    with st.expander("View temporary file details"):
        for i, temp_file in enumerate(st.session_state.get("temp_files", [])):
            file_exists = os.path.exists(temp_file)
            file_size = ""
            if file_exists:
                try:
                    size_bytes = os.path.getsize(temp_file)
                    file_size = f" ({size_bytes} bytes)"
                except Exception:
                    file_size = "(size unknown), "

            st.code(f"{i + 1}. {temp_file}{file_size}")
            if not file_exists:
                st.caption("⚠️ File no longer exists")
else:
    st.caption("No temporary files currently stored.")

st.divider()

# Export Options
st.header("Export Chat")
if st.session_state.get("messages"):
    # Create a markdown string from the chat history
    chat_export_md = ""
    for msg in st.session_state.messages:
        role = msg["role"].title()
        content = msg["content"]

        # Handle multimodal content
        if isinstance(content, list):
            text_parts = []
            image_count = 0
            for item in content:
                if item["type"] == "text":
                    if not item["text"].startswith("Uploaded image file paths:"):
                        text_parts.append(item["text"])
                elif item["type"] == "image_url":
                    image_count += 1

            content_str = " ".join(text_parts)
            if image_count > 0:
                content_str += f" [Contains {image_count} image(s)]"
            chat_export_md += f"**{role}**: {content_str}\n\n"
        else:
            chat_export_md += f"**{role}**: {content}\n\n"

    st.download_button(
        "Download as Markdown (.md)",
        chat_export_md,
        "chat_history.md",
        "text/markdown",
    )

    # Create a JSON string from the chat history (excluding base64 image data for size)
    export_messages = []
    for msg in st.session_state.messages:
        if isinstance(msg["content"], list):
            # Filter out base64 image data for export
            filtered_content = []
            for item in msg["content"]:
                if item["type"] == "text":
                    filtered_content.append(item)
                elif item["type"] == "image_url":
                    filtered_content.append(
                        {
                            "type": "image_url",
                            "image_url": "[IMAGE DATA REMOVED FOR EXPORT]",
                        }
                    )
            export_messages.append({"role": msg["role"], "content": filtered_content})
        else:
            export_messages.append(msg)

    chat_export_json = json.dumps(export_messages, indent=2)
    st.download_button(
        "Download as JSON (.json)",
        chat_export_json,
        "chat_history.json",
        "application/json",
    )
else:
    st.caption("No messages to export yet. Start a conversation first!")

st.divider()

# Clear Chat Option
st.header("Clear Chat")
if st.session_state.get("messages"):
    st.warning(
        "⚠️ **This will permanently delete your chat history from all devices and clean up temporary files.**"
    )
    st.caption(
        "This action cannot be undone and will affect your chat history across all devices."
    )

    if st.button("🗑️ Clear All Chat History", type="secondary"):
        with st.spinner("Clearing chat history..."):
            # Clean up temp files first
            cleanup_temp_files()

            # Clear thread history from database
            thread_cleared = clear_thread_history()

            if thread_cleared:
                # Clear local session messages
                st.session_state.messages = []

                # Reset history loaded flag so it can be reloaded (empty) next time
                if "history_loaded" in st.session_state:
                    st.session_state.history_loaded = False

                st.success("✅ Chat history completely cleared from all devices!")
            else:
                st.error(
                    "❌ Failed to clear thread history from database. Local session cleared."
                )
                # Still clear local session even if database clearing failed
                st.session_state.messages = []

        st.rerun()
else:
    st.caption("No chat history to clear.")

st.divider()

# Thread Information (for debugging/info)
st.header("Thread Information")
thread_id = st.session_state.get("user_email", "default")
st.code(f"Thread ID: {thread_id}")
st.caption("Your chat history is stored using your email as the thread identifier.")
